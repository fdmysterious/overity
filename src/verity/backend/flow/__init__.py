"""
VERITY Method flow management
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import atexit
import logging
import tempfile
import sys

from pathlib import Path

from datetime import datetime as dt
from dataclasses import dataclass

from verity.backend import program
from verity.storage.local import LocalStorage

from verity.model.general_info.method import MethodKind
from verity.model.report import MethodReport

from verity.model.ml_model.metadata import (
    MLModelAuthor,
    MLModelMaintainer,
    MLModelMetadata,
)
from verity.model.ml_model.package import MLModelPackage

from verity.model.traceability import (
    ArtifactKind,
    ArtifactKey,
    ArtifactLinkKind,
    ArtifactLink,
)

from verity.exchange import report_json
from verity.exchange.method_common import file_py, file_ipynb
from verity.errors import UnidentifiedMethodError, UninitAPIError

from verity.backend.flow.ctx import FlowCtx, RunMode
from verity.backend.flow.arguments import ArgumentParser

from contextlib import contextmanager


log = logging.getLogger("backend.flow")


class LogArrayHandler(logging.Handler):
    def __init__(self, report: MethodReport):
        super().__init__()

        self.report = report

    def emit(self, record):
        self.report.log_add(
            tstamp=dt.now(),
            severity=record.levelname,
            source=f"{record.filename}:{record.lineno}",
            message=record.getMessage(),
        )


class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        message = message.strip()

        # Remove any trailing newlines to avoid empty log entries
        if message not in ["", "^"]:
            self.logger.log(self.level, message.strip())

    def flush(self):
        # Flush method is required but can be a no-op
        pass


@dataclass
class ModelPackageInfo:
    model_metadata: MLModelMetadata
    model_file_path: Path  # Path to store model file
    inference_example_path: Path  # Optional folder path to store inference example


def _api_guard(fkt):
    def call(ctx, *args, **kwargs):
        if not ctx.init_ok:
            raise UninitAPIError()
        else:
            return fkt(ctx, *args, **kwargs)

    return call


def init(ctx: FlowCtx, method_path: Path, run_mode: RunMode):
    log.info(f"Initialize API for method {method_path}")
    date_started = dt.now()

    # Set run mode
    ctx.run_mode = run_mode
    log.info(f"Running in mode: {run_mode}")

    # Get current programme
    ctx.pdir = program.find_current(start_path=method_path.parent)
    log.info(f"Programme directory: {ctx.pdir}")

    # Init local storage
    ctx.storage = LocalStorage(ctx.pdir)

    # Identify method slug and kind
    ctx.method_path = method_path
    ctx.method_slug = ctx.storage.identify_method_slug(method_path)
    ctx.method_kind = ctx.storage.identify_method_kind(method_path)

    # Read method information
    ctx.method_info = method_info_get(ctx)  # Read method information from file

    log.info(f"Method identification: {ctx.method_slug} ({ctx.method_kind.value})")

    # Initialize report and environment information
    ctx.report = MethodReport.default(
        uuid=ctx.storage.method_report_uuid_get(ctx.method_kind),
        date_started=date_started,
    )

    # Initialize run traceability information
    # TODO: For other types
    if ctx.method_kind == MethodKind.TrainingOptimization:
        ctx.report.method_key = ArtifactKey(
            kind=ArtifactKind.TrainingOptimizationMethod, id=ctx.method_slug
        )
        ctx.report.report_key = ArtifactKey(
            kind=ArtifactKind.OptimizationReport, id=ctx.report.uuid
        )
        ctx.report.run_key = ArtifactKey(
            kind=ArtifactKind.OptimizationRun, id=ctx.report.uuid
        )

        # Add link between run and report
        ctx.report.traceability_graph.add(
            ArtifactLink(
                a=ctx.report.report_key,
                b=ctx.report.run_key,
                kind=ArtifactLinkKind.ReportFor,
            )
        )

        # Add link between run and method
        ctx.report.traceability_graph.add(
            ArtifactLink(
                a=ctx.report.run_key,
                b=ctx.report.method_key,
                kind=ArtifactLinkKind.MethodUse,
            )
        )

    # Initialize logger
    root_log = logging.getLogger("")
    root_log.addHandler(LogArrayHandler(report=ctx.report))

    stdout_log = logging.getLogger("stdout")
    stderr_log = logging.getLogger("stderr")

    # Redirect stdout and stderr...
    sys.stdout = LoggerWriter(stdout_log, logging.INFO)
    sys.stderr = LoggerWriter(stderr_log, logging.ERROR)

    # Add exit handler to save report file
    atexit.register(lambda: exit_handler(ctx))

    # Init is done!
    ctx.init_ok = True


def exit_handler(ctx: FlowCtx):
    log.info("Exiting method execution")

    # Set end date
    ctx.report.date_ended = dt.now()

    # Save report file
    output_path = ctx.storage.method_run_report_path(ctx.report.uuid, ctx.method_kind)
    log.info(f"Save output report to {output_path}")

    report_json.to_file(ctx.report, output_path)


def method_info_get(ctx):
    if ctx.method_path.suffix == ".py":
        return file_py.from_file(ctx.method_path, kind=ctx.method_kind)
    elif ctx.method_path.suffix == ".ipynb":
        return file_ipynb.from_file(ctx.method_path, kind=ctx.method_kind)
    else:
        raise UnidentifiedMethodError(ctx.method_kind)


@_api_guard
@contextmanager
def describe_arguments(ctx):
    parser = ArgumentParser(ctx)

    yield parser

    # Parse arguments
    log.info("Parse arguments")
    parser.parse_args()

    ctx.args = parser.context()

    # Save context information
    ctx.report.context = ctx.args


@_api_guard
def argument(ctx, name: str):
    return ctx.args[name]


@_api_guard
def model_use(ctx, slug: str):
    log.info(f"Search for model: {slug}")

    tmpdir = tempfile.TemporaryDirectory()
    tmpdir_path = Path(tmpdir.name).resolve()

    pkginfo = ctx.storage.model_load(slug, tmpdir_path)

    # Add traceability TODO
    # -> Create artifact key for model
    model_key = ArtifactKey(
        kind=ArtifactKind.Model,
        id=slug,
    )

    # -> Model use for optimization run
    ctx.report.traceability_graph.add(
        ArtifactLink(
            a=ctx.report.run_key,
            b=model_key,
            kind=ArtifactLinkKind.ModelUse,
        )
    )

    ctx.tmpdirs.append(tmpdir)

    return tmpdir_path / pkginfo.model_file, pkginfo


@_api_guard
@contextmanager
def model_package(
    ctx: FlowCtx, slug: str, exchange_format: str, target: str = "agnostic"
):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize package metadata
        meta = MLModelMetadata(
            name=slug,
            version="TODO",  # TODO: How to treat this?
            authors=[
                MLModelAuthor(name=a.name, email=a.email, contribution=a.contribution)
                for a in ctx.method_info.authors
            ],
            # TODO: How to determine list of maintainers? Maybe store as program information?
            maintainers=[
                MLModelMaintainer(name=a.name, email=a.email)
                for a in ctx.method_info.authors
            ],
            target=target,
            exchange_format=exchange_format,
            model_file=f"model.{exchange_format}",
        )

        # Initialize context information
        pkginfo = ModelPackageInfo(
            model_metadata=meta,
            model_file_path=Path(tmpdir).resolve() / meta.model_file,
            inference_example_path=Path(tmpdir).resolve() / "inference-example",
        )

        yield pkginfo

        # -> Now the user should have stored files...
        # TODO: Add check that model file is effectively stored here, or else raise some exception

        # Create traceability information
        model_key = ArtifactKey(
            kind=ArtifactKind.Model,
            id=slug,
        )

        ctx.report.traceability_graph.add(
            ArtifactLink(
                a=ctx.report.run_key,
                b=model_key,
                kind=ArtifactLinkKind.ModelGeneratedBy,
            )
        )

        # Now that package is created, we can create the archive
        ctx.storage.model_store(
            slug,
            MLModelPackage(
                metadata=meta,
                model_file_path=pkginfo.model_file_path,
                example_implementation_path=(
                    pkginfo.inference_example_path
                    if pkginfo.inference_example_path.exists()
                    else None
                ),
            ),
        )

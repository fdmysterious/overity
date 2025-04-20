"""
VERITY Method flow management
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import atexit
import logging
from dataclasses import dataclass
from pathlib import Path

from datetime import datetime as dt

from verity.backend import program
from verity.storage.local import LocalStorage

from verity.model.general_info.method import MethodKind
from verity.model.report import MethodReport

from verity.model.traceability import (
    ArtifactKind,
    ArtifactKey,
    ArtifactLinkKind,
    ArtifactLink,
)

from verity.exchange import report_json


log = logging.getLogger("backend.flow")


@dataclass
class FlowCtx:
    pdir: Path  # Path to current programme
    init_ok: bool  # Is Flow init OK?
    storage: LocalStorage
    report: MethodReport

    method_slug: str
    method_kind: MethodKind

    method_key: ArtifactKey  # Helps identify the current method key for traceability
    report_key: ArtifactKey
    run_key: ArtifactKey

    @classmethod
    def default(cls):
        return cls(
            pdir=None,
            init_ok=False,
            storage=None,
            report=None,
            method_slug=None,
            method_kind=None,
            method_key=None,
            report_key=None,
            run_key=None,
        )


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


def init(ctx: FlowCtx, method_path: Path):
    log.info(f"Initialize API for method {method_path}")
    date_started = dt.now()

    # Get current programme
    ctx.pdir = program.find_current(start_path=method_path.parent)
    log.info(f"Programme directory: {ctx.pdir}")

    # Init local storage
    ctx.storage = LocalStorage(ctx.pdir)

    # Identify method slug and kind
    ctx.method_slug = ctx.storage.identify_method_slug(method_path)
    ctx.method_kind = ctx.storage.identify_method_kind(method_path)

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

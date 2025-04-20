"""
VERITY report encoder/decoder
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import json

from pathlib import Path
from verity.model.report import MethodReportLogItem, MethodReport
from verity.model.traceability import ArtifactKey, ArtifactGraph


# --------------------------- Encoder


def _encode_artifact_key(x: ArtifactKey) -> dict[str, str]:
    return {
        "kind": x.kind.value,
        "id": x.id,
    }


def _encode_traceability_graph(gr: ArtifactGraph) -> list[dict[str, str]]:
    def do_item(x):
        return {
            "a": _encode_artifact_key(x.a),
            "b": _encode_artifact_key(x.b),
            "kind": x.kind.value,
        }

    return list(map(do_item, gr.links))


def _encode_logs(x: list[MethodReportLogItem]) -> list[dict[str, str]]:
    def do_item(x):
        return {
            "dt": x.timestamp.isoformat(),
            "severity": x.severity,
            "source": x.source,
            "message": x.message,
        }

    return list(map(do_item, x))


def to_file(report: MethodReport, path: Path):
    output_obj = {
        "uuid": report.uuid,
        "date_started": report.date_started.isoformat(),
        "date_ended": report.date_ended.isoformat(),
        "environment": report.environment,
        "context": report.context,
        "traceability_graph": _encode_traceability_graph(report.traceability_graph),
        "logs": _encode_logs(report.logs),
        # outputs TODO #
    }

    with open(path, "w") as fhandle:
        json.dump(output_obj, fhandle)


# --------------------------- Decoder

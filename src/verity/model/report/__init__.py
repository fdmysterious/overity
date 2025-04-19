"""
VERITY model for reports
========================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations


from dataclasses import dataclass
from datetime import datetime

from verity.model.traceability import ArtifactGraph


@dataclass
class MethodReportLogItem:
    timestamp: datetime
    severity: str
    source: str
    message: str


@dataclass
class MethodReport:
    uuid: str
    date_started: datetime
    date_ended: datetime
    environment: dict[str, str]
    context: dict[str, str]
    traceability_graph: ArtifactGraph
    logs: list[MethodReportLogItem]
    outputs: any | None = None

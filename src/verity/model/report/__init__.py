"""
VERITY model for reports
========================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

from datetime import datetime as dt
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

    @classmethod
    def default(cls, uuid: str, date_started: dt | None = None) -> MethodReport:
        date_started = date_started or dt.now()

        return cls(
            uuid=uuid,
            date_started=date_started,
            date_ended=None,
            environment={},
            context={},
            traceability_graph=ArtifactGraph.default(),
            logs=[],
            outputs=None,
        )

    def log_add(self, tstamp: dt, severity: str, source: str, message: str):
        self.logs.append(
            MethodReportLogItem(
                timestamp=tstamp,
                severity=severity,
                source=source,
                message=message,
            )
        )

"""
VERITY flow context
===================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from verity.model.general_info.Method import MethodKind
from verity.storage.local import LocalStorage
from verity.model.report import MethodReport
from verity.model.traceability import ArtifactKey


@dataclass
class FlowCtx:
    pdir: Path  # Path to current programme
    init_ok: bool  # Is Flow init OK?
    storage: LocalStorage
    report: MethodReport

    method_path: Path  # Path to current method
    method_slug: str
    method_kind: MethodKind

    method_key: ArtifactKey  # Helps identify the current method key for traceability
    report_key: ArtifactKey
    run_key: ArtifactKey

    args: dict[str, str]

    @classmethod
    def default(cls):
        return cls(
            pdir=None,
            init_ok=False,
            storage=None,
            report=None,
            method_path=None,
            method_slug=None,
            method_kind=None,
            method_key=None,
            report_key=None,
            run_key=None,
            args=None,
        )

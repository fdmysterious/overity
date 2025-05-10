"""
Backend operations on reports
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- May 2025
"""

import logging

from pathlib import Path

from verity.model.report import MethodReportKind
from verity.storage.local import LocalStorage

log = logging.getLogger("backend.report")


def load(pdir: Path, kind: MethodReportKind, identifier: str):
    log.info(
        f"Load report '{identifier}' of kind '{kind.value}' from program stored at {pdir}"
    )

    st = LocalStorage(pdir)
    return st.report_load(kind, identifier)

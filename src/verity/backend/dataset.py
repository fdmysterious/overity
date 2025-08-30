"""
Verity dataset backend features
===============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- August 2025
"""

import logging
from pathlib import Path

from verity.storage.local import LocalStorage

log = logging.getLogger("backend.dataset")


def list_datasets(program_path: Path):
    """List the current available datasets"""

    program_path = Path(program_path)

    log.info(f"List avialalbe datasets from program {program_path}")
    st = LocalStorage(program_path)

    datasets, errors = st.datasets()

    return datasets, errors

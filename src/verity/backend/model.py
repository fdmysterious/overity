"""
Verity model backend features
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging

from pathlib import Path

from verity.storage.local import LocalStorage

log = logging.getLogger("backend.model")


def list_models(program_path: Path):
    """List the current available models"""

    program_path = Path(program_path).resolve()

    log.info(f"List models from program {program_path}")
    st = LocalStorage(program_path)

    models, errors = st.models()

    return models, errors

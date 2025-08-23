"""
Verity inference agents backend features
========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- August 2025
"""

import logging
from pathlib import Path

from verity.storage.local import LocalStorage

log = logging.getLogger("backend.inference_agents")


def list_agents(program_path: Path):
    """List the current available inference agents"""

    program_path = Path(program_path)

    log.info(f"List inference agents from program {program_path}")
    st = LocalStorage(program_path)

    agents, errors = st.inference_agents()

    return agents, errors

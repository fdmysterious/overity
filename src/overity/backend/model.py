"""
Overity.ai model backend features
=============================

**April 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the LGPL 3.0 license. See the LICENSE file for more
> information.
"""

import logging

from pathlib import Path

from overity.storage.local import LocalStorage

log = logging.getLogger("backend.model")


def list_models(program_path: Path):
    """List the current available models"""

    program_path = Path(program_path).resolve()

    log.info(f"List models from program {program_path}")
    st = LocalStorage(program_path)

    models, errors = st.models()

    return models, errors

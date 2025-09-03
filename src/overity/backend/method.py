"""
Overity.ai methods backend features
===================================

**April 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

import logging
from pathlib import Path

from overity.storage.local import LocalStorage


log = logging.getLogger("backend.methods")


def list_topt_methods(program_path: Path | str):
    """List the current available training/optimization methods from the given program path"""

    program_path = Path(program_path).resolve()

    log.info(f"List training/optimization methods from program in {program_path}")
    st = LocalStorage(program_path)
    methods, errors = st.training_optimization_methods()

    return methods, errors

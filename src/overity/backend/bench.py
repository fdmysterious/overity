"""
Overity.ai bench management backend features
============================================

**September 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

import logging
from pathlib import Path

from overity.storage.local import LocalStorage

log = logging.getLogger("backend.bench")


def list_benches(program_path: Path):
    """List available bench instanciations in program"""

    program_path = Path(program_path)

    log.info(f"List bench instanciations from program {program_path}")
    st = LocalStorage(program_path)

    benches, errors = st.benches()

    return benches, errors

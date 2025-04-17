"""
# Verity program backend features

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

import logging
from pathlib import Path

from verity.backend.errors import ProgramNotFound
from verity.storage.local import LocalStorage

log = logging.getLogger("backend.program")


########################################
# Find program.toml file
########################################


def is_program(path: Path):
    """Indicates if the current folder is the root folder of a program"""
    return (path / "program.toml").is_file()


def _iter_path(pp: Path):
    """Iterate path from cwd to filesystem root, generator style!"""

    cur_path = pp

    while True:
        yield cur_path

        if cur_path.parent != cur_path:
            cur_path = cur_path.parent
        else:
            break


def find_current(start_path: Path):
    log.debug(f"Search program root folder starting from {start_path}")

    if is_program(start_path):
        return start_path

    else:
        for subpath in _iter_path(start_path.parent):
            log.debug(f"Check parent path: {subpath}")

            if is_program(subpath):
                return subpath

        raise ProgramNotFound(start_path=start_path, recursive=True)


def infos(path: Path):
    """Load program information"""

    path = Path(path).resolve()

    log.info(f"Load program information from {path}")

    st = LocalStorage(path)

    return st.program_info()

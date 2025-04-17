"""
Parse method information from jupyter notebook
==============================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import nbformat

from pathlib import Path

from verity.errors import EmptyMethodDescription
from verity.exchange.method_common import description_md


# --------------------------- Private interface


def _extract_first_md_cell(path: Path):
    path = Path(path)

    with open(path, "r") as fhandle:
        nb = nbformat.read(fhandle, as_version=4)

    return next(filter(lambda x: x["cell_type"] == "markdown", nb["cells"]))


# --------------------------- Public interface


def from_file(path: Path):
    path = Path(path)

    try:
        md_desc = _extract_first_md_cell(path=path)
        md_text = "".join(md_desc["source"])

        if not md_text:
            raise EmptyMethodDescription(file_path=path)

        infos = description_md.from_md_desc(md_text)

        return infos

    except StopIteration:
        raise EmptyMethodDescription(file_path=path)

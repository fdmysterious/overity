"""
Parse method information from python file
=========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import ast
from pathlib import Path

from verity.errors import EmptyMethodDescription
from verity.exchange.method_common import description_md

# --------------------------- Private interface


def _read_docstring(path: Path):
    source = Path(path).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            return ast.get_docstring(node)

    return None


# --------------------------- Public interface


def from_file(path: Path):
    docstr = _read_docstring(path)

    if docstr is not None:
        return description_md.from_md_desc(docstr)

    else:
        raise EmptyMethodDescription(file_path=path)

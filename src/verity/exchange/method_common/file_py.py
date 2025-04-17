"""
Parse method information from python file
=========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import ast
from pathlib import Path

from verity.model.general_info.method import MethodKind
from verity.errors import EmptyMethodDescription
from verity.exchange.method_common import description_md

# --------------------------- Private interface


def _extract_slug(path: Path):
    path = Path(path)
    slug = path.stem

    return slug


def _read_docstring(path: Path):
    source = Path(path).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            return ast.get_docstring(node)

    return None


# --------------------------- Public interface


def from_file(path: Path, kind: MethodKind):
    docstr = _read_docstring(path)
    slug = _extract_slug(path)

    if docstr is not None:
        return description_md.from_md_desc(
            x=docstr, slug=slug, kind=kind, file_path=path
        )

    else:
        raise EmptyMethodDescription(file_path=path)

"""
Parse method information from python file
=========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations


from textwrap   import dedent
from pathlib    import Path

import ast

from verity.model.general_info.method import (
    MethodKind,
    MethodAuthor,
    MethodInfo,
)


from verity.exchange.method_common import description_md
from verity.errors import EmptyMethodDescription


# --------------------------- Private interface

def _read_docstring(path: Path):
    source = Path(path).read_text()
    tree   = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            return ast.get_docstring(node)

    else:
        return None


# --------------------------- Public interface

def from_file(path: Path):
    docstr = _read_docstring(path)

    if docstr is not None:
        method_info = description_md.from_md_desc(docstr)
        return method_info

    else: raise EmptyMethodDescription(file_path=path)

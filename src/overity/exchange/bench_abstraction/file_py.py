"""
Parser for bench abstraction definition
=======================================

**September 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

from __future__ import annotations

import ast

from pathlib import Path
from overity.exchange.bench_abstraction import description_md

from overity.errors import EmptyMethodDescription


####################################################
# Private interface
####################################################


def _extract_slug(path: Path):
    path = Path(path)
    slug = path.name.removesuffix(".py")

    return slug


def _read_docstring(path: Path):
    source = Path(path).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            return ast.get_docstring(node)

    return None


####################################################
# Public interface
####################################################


def from_file(path: Path):
    docstr = _read_docstring(path)
    slug = _extract_slug(path)

    if docstr is not None:
        return description_md.from_md_desc(x=docstr, slug=slug, file_path=path)
    else:
        raise EmptyMethodDescription(file_path=path)  # TODO # Use another exception?

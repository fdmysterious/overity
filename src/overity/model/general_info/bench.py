"""
Bench abstraction and instanciation metadata definition
=======================================================

**June 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class BenchAbstractionAuthor:
    """Describes an author for a bench abstraction"""

    """Name of the author"""
    name: str

    """Email of the author"""
    email: str

    """Optional contribution details"""
    contribution: str | None = None


@dataclass
class BenchAbstractionMetadata:
    """Metadata associated with a bench abstraction"""

    """Bench abstraction identification"""
    slug: str

    """Display name"""
    display_name: str

    """Authors"""
    authors: list[BenchAbstractionAuthor]

    """Optional metadata fields"""
    metadata: dict[str, str]

    """Optional description"""
    description: str | None = None

    def __hash__(self):
        return hash(self.slug)


@dataclass
class BenchInstanciationMetadata:
    """Metadata associated with a bench instanciation"""

    """Bench instanciation slug"""
    slug: str

    """Display name"""
    display_name: str

    """Associated bench abstraction slug"""
    abstraction_slug: str

    """Used parameter values for bench instanciation"""
    settings: dict[str, str | bool | float | int] | None = None

    """Optional bench description"""
    description: str | None = None

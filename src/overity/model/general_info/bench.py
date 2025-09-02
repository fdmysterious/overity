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

from overity.model.general_info.capability import Capability


@dataclass
class BenchAbstractionMetadata:
    """Metadata associated with a bench abstraction"""

    """Bench abstraction identification"""
    slug: str

    """Display name"""
    display_name: str

    """Bench capabilities list"""
    capabilities: frozenset[Capability]

    """List of compatible tags"""
    compatible_tags: frozenset[str]

    """List of compatible execution targets"""
    compatible_targets: frozenset[str]

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

    """Associated bench abstraction metadata"""
    bench_abstraction: BenchAbstractionMetadata

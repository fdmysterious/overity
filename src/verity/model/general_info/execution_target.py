"""
Execution target information

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

from dataclasses import dataclass
from typing import FrozenSet, Optional


@dataclass
class ExecutionTarget:
    """An execution target identifies on which target a model can be deployed"""

    """Slug acts as a text identifier for the execution target"""
    slug: str

    """Display name for Execution target"""
    display_name: str

    """Tags can help idnetify this target among others.

    Example tags can be: SoC, MCU, etc.
    """
    tags: FrozenSet[str]

    """Optional description text."""
    description: Optional[str] = None

    def __hash__(self):
        return hash(self.slug)

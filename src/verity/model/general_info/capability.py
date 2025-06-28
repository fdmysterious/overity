"""
Model class for bench capability identification

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- June 2025
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Capability:
    """Identifies a requirement on a test bench

    For instance, it can represent the bench ability to measure energy consumption per inference.
    A capability is associated with a requirement into what the bench should provide, i.e. a
    given metric or a specific method.
    """

    """Identifier of the capability"""
    slug: str

    """Display name"""
    display_name: str

    """Optional description"""
    description: str | None = None

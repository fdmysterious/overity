"""
# Model class for program information

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ProgramInitiator:
    """A program initiator is is responsible for the initialization of the program."""

    """Name of person"""
    name: str

    """Email of person"""
    email: str

    """Optional role for this person in its organization"""
    role: Optional[str] = None


@dataclass
class ProgramInfo:
    """Information for a program"""

    """The slug is the recognizable unique identifier for the program"""
    slug: str

    """Display name represents a more readable name for user display"""
    display_name: str

    """Program creation date"""
    date_created: date

    """Who initiated this program"""
    initiator: ProgramInitiator

    """Is the program active?"""
    active: bool

    """An optioanl description can act as a tagline to tell what the program is for"""
    description: Optional[str] = None

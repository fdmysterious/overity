"""
Model to store arguments when using methods
===========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Argument:
    name: str
    value: str


@dataclass
class Option:
    name: str
    value: str | None
    default: str


@dataclass
class Flag:
    name: str
    value: bool


@dataclass(frozen=True)
class ArgumentSchema:
    name: str
    help: str


@dataclass(frozen=True)
class OptionSchema:
    name: str
    default: str
    help: str


@dataclass(frozen=True)
class FlagSchema:
    name: str
    help: str

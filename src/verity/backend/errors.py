"""
# Verity backend errors

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

from pathlib import Path


class ProgramNotFound(Exception):
    def __init__(self, start_path: Path, recursive: bool = False):
        super().__init__(
            f"No program storage found starting from {start_path}. Recursive search was {'on' if recursive else 'off'}"
        )

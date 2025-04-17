"""
VERITY-AI toolkit errors
========================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from pathlib import Path

class EmptyMethodDescription(Exception):
    def __init__(self, file_path: Path):
        super().__init__(f"No method description found in file: {file_path!s}")
        self.file_path = file_path

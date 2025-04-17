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


class ProgramNotFound(Exception):
    def __init__(self, start_path: Path, recursive: bool = False):
        super().__init__(
            f"No program storage found starting from {start_path}. Recursive search was {'on' if recursive else 'off'}"
        )


class DuplicateSlugError(Exception):
    def __init__(self, path: Path, slug: str):
        super().__init__(f"Duplicate slug found in {path!s}: {slug!s}")

        self.path = path
        self.slug = slug

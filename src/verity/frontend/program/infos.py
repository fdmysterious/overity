"""
# Show program informations

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

import logging
import traceback
from argparse import ArgumentParser, Namespace
from pathlib import Path

from verity.backend import program as program_backend
from verity.backend.errors import ProgramNotFound

log = logging.getLogger("frontend.program.infos")


def setup_parser(parser: ArgumentParser):
    parser.add_parser("infos", help="Get informations on program in current folder")


def run(args: Namespace):
    cwd = Path.cwd()

    try:
        pdir = program_backend.find_current(start_path=cwd)
        prginfo = program_backend.infos(pdir)

        if prginfo.description is not None:
            pass

    except ProgramNotFound as exc:
        log.exception(str(exc))
        log.debug(traceback.format_exc())

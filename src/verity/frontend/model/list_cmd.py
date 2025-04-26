"""
List available models for a given programme
===========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging
import traceback

from argparse import ArgumentParser, Namespace
from pathlib import Path

from verity.backend import program as b_program
from verity.errors import ProgramNotFound


log = logging.getLogger("frontend.method.list_cmd")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser("list", aliases=["ls"], help="List available models")

    return subcommand


def run(args: Namespace):
    cwd = Path.cwd()

    try:
        pdir = b_program.find_current(start_path=cwd)
        print(pdir)

    except ProgramNotFound as exc:
        log.exception(str(exc))
        log.debug(traceback.format_exc())

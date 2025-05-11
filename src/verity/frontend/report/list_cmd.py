"""
List reports of a given kind for a program
==========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- May 2025
"""

import logging

from argparse import ArgumentParser, Namespace
from pathlib import Path

from verity.backend import report as b_report
from verity.backend import program as b_program
from verity.frontend import types


log = logging.getLogger("frontend.report.list")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "list", aliases=["ls"], help="List reports of a certain kind"
    )

    subcommand.add_argument(
        "kind", type=types.parse_report_kind, help="What report kind to list"
    )
    subcommand.add_argument(
        "--all",
        dest="include_all",
        action="store_true",
        help="Include reports with failed status",
    )

    return subcommand


def run(args: Namespace):
    cwd = Path.cwd()
    pdir = b_program.find_current(start_path=cwd)
    reports = b_report.list(pdir, kind=args.kind, include_all=args.include_all)

    for rp in reports:
        print(rp)

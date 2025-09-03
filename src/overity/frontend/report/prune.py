"""
Overity.ai command to prune unsucessful reports
===============================================

**May 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

import logging

from argparse import ArgumentParser, Namespace
from pathlib import Path

from overity.backend import report as b_report
from overity.backend import program as b_program

from overity.frontend import types

log = logging.getLogger("frontend.report.prune")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "prune", help="Remove reports that are not succesful"
    )
    subcommand.add_argument(
        "kind", type=types.parse_report_kind, help="What report kind to prune"
    )

    return subcommand


def run(args: Namespace):
    cwd = Path.cwd()
    pdir = b_program.find_current(start_path=cwd)

    reports_ok = b_report.list(pdir, kind=args.kind, include_all=False)
    reports_all = b_report.list(pdir, kind=args.kind, include_all=True)

    reports_to_remove = frozenset(reports_all) - frozenset(reports_ok)

    for report in reports_to_remove:
        print(report)
        b_report.remove(pdir, args.kind, report)

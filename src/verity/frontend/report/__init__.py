"""
VERITY frontend commands to manipulate reports
==============================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- May 2025
"""

from argparse import ArgumentParser, Namespace

from verity.frontend.report import view

CLI_SUBCOMMANDS = {view}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "report", aliases=["rpt"], help="Report manipulation"
    )
    subparsers = subcommand.add_subparsers(dest="report_subcommand")

    for cmd in CLI_SUBCOMMANDS:
        subp = cmd.setup_parser(subparsers)
        subp.set_defaults(report_subcommand_clbk=cmd)

    return subcommand


def run(args: Namespace):
    if hasattr(args, "report_subcommand_clbk"):
        args.report_subcommand_clbk.run(args)

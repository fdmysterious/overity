"""
Command subgroup for methods related manipulations
==================================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from argparse import ArgumentParser, Namespace

from verity.frontend.method import list_cmd

CLI_SUBCOMMANDS = {"list": list_cmd}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "method", aliases=["mtd"], help="Method manipulation"
    )
    subparsers = subcommand.add_subparsers(dest="method_subcommand")

    for cmd in CLI_SUBCOMMANDS.values():
        cmd.setup_parser(subparsers)


def run(args: Namespace):
    k_cmd = args.method_subcommand

    if k_cmd in CLI_SUBCOMMANDS:
        CLI_SUBCOMMANDS[k_cmd].run(args)

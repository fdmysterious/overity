"""
Command subgroup for dataset related manipulations
==================================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- August 2025
"""

from argparse import ArgumentParser, Namespace

from verity.frontend.dataset import list_cmd

CLI_SUBCOMMANDS = {list_cmd}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "dataset", aliases=["data"], help="Dataset manipulation"
    )
    subparsers = subcommand.add_subparsers(dest="dataset_subcommand")

    for cmd in CLI_SUBCOMMANDS:
        subp = cmd.setup_parser(subparsers)
        subp.set_defaults(dataset_subcommand_clbk=cmd)

    return subcommand


def run(args: Namespace):
    if hasattr(args, "dataset_subcommand_clbk"):
        args.dataset_subcommand_clbk.run(args)

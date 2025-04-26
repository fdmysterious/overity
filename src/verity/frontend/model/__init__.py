"""
Command subgroup for models related manipulations
=================================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from argparse import ArgumentParser, Namespace

from verity.frontend.model import list_cmd

CLI_SUBCOMMANDS = {list_cmd}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser("model", aliases=["mod"], help="Model manipulation")
    subparsers = subcommand.add_subparsers(dest="model_subcommand")

    for cmd in CLI_SUBCOMMANDS:
        subp = cmd.setup_parser(subparsers)
        subp.set_defaults(method_subcommand_clbk=cmd)

    return subcommand


def run(args: Namespace):
    if hasattr(args, "model_subcommand_clbk"):
        args.method_subcommand_clbk.run(args)

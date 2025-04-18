"""
# Command subgroup for program related manipulation

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace

from verity.frontend.program import infos

CLI_SUBCOMMANDS = {"infos": infos}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "program", aliases=["prg"], help="Program manipulation"
    )
    subparsers = subcommand.add_subparsers(dest="program_subcommand")

    for cmd in CLI_SUBCOMMANDS.values():
        cmd.setup_parser(subparsers)

    return subcommand


def run(args: Namespace):
    k_cmd = args.program_subcommand

    if k_cmd in CLI_SUBCOMMANDS:
        CLI_SUBCOMMANDS[k_cmd].run(args)

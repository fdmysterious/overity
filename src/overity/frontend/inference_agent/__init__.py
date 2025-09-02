"""
Command subgroup for inference agents related manipulations
===========================================================

**August 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

from argparse import ArgumentParser, Namespace

from overity.frontend.inference_agent import list_cmd

CLI_SUBCOMMANDS = {list_cmd}


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "agent", aliases=["agt"], help="Inference agent manipulation"
    )
    subparsers = subcommand.add_subparsers(dest="agent_subcommand")

    for cmd in CLI_SUBCOMMANDS:
        subp = cmd.setup_parser(subparsers)
        subp.set_defaults(agent_subcommand_clbk=cmd)

    return subcommand


def run(args: Namespace):
    if hasattr(args, "agent_subcommand_clbk"):
        args.agent_subcommand_clbk.run(args)

"""
Verity commands for CLI
=======================

**February 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the LGPL 3.0 license. See the LICENSE file for more
> information.
"""

import sys

from verity.frontend import program
from verity.frontend import method
from verity.frontend import model
from verity.frontend import inference_agent
from verity.frontend import dataset
from verity.frontend import report


CLI_GROUPS = {program, method, model, inference_agent, report, dataset}


def main():
    # TODO: Setup logger
    # logging.basicConfig(level=logging.DEBUG)

    # Imports and initial setup
    import argparse

    # Setup argument parser
    parser = argparse.ArgumentParser(
        prog="verity",
        description="Toolkit for AI training, optimization and validation on embedded systems",
    )

    cmdgroup = parser.add_subparsers(dest="cmdgroup")

    for cmd in CLI_GROUPS:
        subp = cmd.setup_parser(cmdgroup)
        subp.set_defaults(target=cmd.run)

    # Parse the arguments
    args = parser.parse_args()

    if (args.cmdgroup is None) or not hasattr(args, "target"):
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        args.target(args)

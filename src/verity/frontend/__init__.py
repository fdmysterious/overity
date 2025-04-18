"""
# Verity commands for CLI

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

import sys

from verity.frontend import program
from verity.frontend import method


CLI_GROUPS = {program, method}


def main():
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

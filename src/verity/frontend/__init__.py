"""
# Verity commands for CLI

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

import sys

from verity.frontend import program
from verity.frontend import method

CLI_GROUPS = {"program": program, "method": method}


def main():
    # Imports and initial setup
    import argparse

    # Setup argument parser
    parser = argparse.ArgumentParser(
        prog="verity",
        description="Toolkit for AI training, optimization and validation on embedded systems",
    )

    cmdgroup = parser.add_subparsers(dest="cmdgroup")

    for cmd in CLI_GROUPS.values():
        cmd.setup_parser(cmdgroup)

    # Parse the arguments
    args = parser.parse_args()

    if args.cmdgroup is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        cmd = CLI_GROUPS[args.cmdgroup]
        cmd.run(args)

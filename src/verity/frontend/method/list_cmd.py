"""
List available methods of a certain kind
========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging
import traceback

from argparse import ArgumentParser, Namespace
from pathlib import Path

from verity.backend import method as b_method
from verity.backend import program as b_program

from verity.errors import ProgramNotFound

from verity.frontend import types
from verity.model.general_info.method import MethodKind

log = logging.getLogger("frontend.method.list_cmd")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "list", aliases=["ls"], help="List available methods of a certain kind"
    )
    subcommand.add_argument(
        "kind", type=types.parse_method_kind, help="What method kind to list"
    )


def run(args: Namespace):
    cwd = Path.cwd()

    try:
        pdir = b_program.find_current(start_path=cwd)

        if args.kind == MethodKind.TrainingOptimization:
            methods, errors = b_method.list_topt_methods(pdir)

            # Display results
            print("")
            for mtd in methods:
                print(f" - {mtd.slug}: {mtd.display_name!r} (in {mtd.path})")

            if errors:
                print("")
                print("While processing, the following errors has been found:")
                for fpath, err in errors:
                    print(f"- in {fpath!s}: {err!s}")

        else:
            log.error(f"Unimplemented kind list: {args.kind}")

    except ProgramNotFound as exc:
        log.exception(str(exc))
        log.debug(traceback.format_exc())

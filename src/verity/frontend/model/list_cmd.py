"""
List available models for a given programme
===========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging
import traceback

from argparse import ArgumentParser, Namespace
from pathlib import Path

from verity.backend import program as b_program
from verity.backend import model as b_model

from verity.errors import ProgramNotFound

from verity.frontend.utils import table as f_table


log = logging.getLogger("frontend.method.list_cmd")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser("list", aliases=["ls"], help="List available models")

    return subcommand


def run(args: Namespace):
    cwd = Path.cwd()

    try:
        pdir = b_program.find_current(start_path=cwd)

        models, errors = b_model.list_models(pdir)

        # Displaying results
        print("")
        print(f"Found the following models in {pdir}:")
        print("")

        headers = ("Model path", "Model name")
        rows = (
            (
                mod_path.relative_to(pdir),
                mod_info.name,
            )
            for mod_path, mod_info in models
        )

        print(f_table.table_format(headers, rows))

        if errors:
            print("")
            print("While processing, the following errors has been found:")
            print("")
            for fpath, err in errors:
                print(f"- in {fpath.relative_to(pdir)!s}: {err!s}")

    except ProgramNotFound as exc:
        log.exception(str(exc))
        log.debug(traceback.format_exc())

"""
# Show program informations

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

import traceback
import textwrap
import logging


from argparse import ArgumentParser, Namespace
from pathlib  import Path

from verity.backend        import program as program_backend
from verity.backend.errors import ProgramNotFound


log = logging.getLogger("frontend.program.infos")


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "infos", help="Get informations on program in current folder"
    )


def run(args: Namespace):
    cwd = Path.cwd()

    try:
        pdir    = program_backend.find_current(start_path = cwd)
        prginfo = program_backend.infos(pdir)

        print("")
        print(f"Program information for '{prginfo.display_name}':")
        print(f" - Slug: {prginfo.slug}")
        print(f" - Created: {prginfo.date_created}")
        print(f" - Initiator: {prginfo.initiator.name} <{prginfo.initiator.email}>{ ' (' + prginfo.initiator.role + ')' if prginfo.initiator.role is not None else ''}")
        print("")

        if prginfo.description is not None:
            print(textwrap.fill(prginfo.description))


    except ProgramNotFound as exc:
        log.error(str(exc))
        log.debug(traceback.format_exc())


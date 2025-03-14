from pathlib import Path
from pprint  import pprint


from verity.backend import program as b_program

import logging


logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()

target_dir = cwd / "storage"


prginfo = b_program.infos(target_dir)

pprint(prginfo)

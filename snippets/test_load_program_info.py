import logging
from pathlib import Path

from verity.backend import program as b_program

logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()

target_dir = cwd / "storage"


prginfo = b_program.infos(target_dir)


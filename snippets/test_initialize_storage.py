from pathlib import Path
from pprint import pprint

from verity.storage.local import LocalStorage

import logging

logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()
target_dir = cwd / "storage"

st = LocalStorage(target_dir)
st.initialize()

prginfo = st.program_info()

pprint(prginfo)

ex_targets = list(st.execution_targets())

pprint(ex_targets)

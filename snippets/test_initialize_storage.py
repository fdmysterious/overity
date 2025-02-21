from pathlib import Path

from verity.storage.local import LocalStorage

import logging

logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()
target_dir = cwd / "storage"

st = LocalStorage(target_dir)
st.initialize()

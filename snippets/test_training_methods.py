import logging
from pathlib import Path
from pprint import pprint

from verity.storage.local import LocalStorage


logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()

target_dir = cwd / "storage"

st = LocalStorage(target_dir)

methods, errors = st.training_optimization_methods()
pprint(methods)
pprint(errors)

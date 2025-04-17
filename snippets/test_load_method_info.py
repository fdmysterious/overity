from pathlib import Path

from verity.exchange.method_common import file_py

cwd = (Path(__file__) / "..").resolve()
test_method = cwd / "storage" / "ingredients" / "training_optimization" / "lstm_init.py"


method_info = file_py.from_file(test_method)


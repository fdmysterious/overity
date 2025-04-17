from pathlib import Path
from pprint import pprint

from verity.model.general_info.method import MethodKind
from verity.exchange.method_common import file_py
from verity.exchange.method_common import file_ipynb

cwd = (Path(__file__) / "..").resolve()
test_method = cwd / "storage" / "ingredients" / "training_optimization" / "lstm_init.py"
test_method2 = cwd / "storage" / "ingredients" / "training_optimization" / "lstm_init.ipynb"


method_info  = file_py.from_file(test_method, kind=MethodKind.TrainingOptimization)
method_info2 = file_ipynb.from_file(test_method2, kind=MethodKind.TrainingOptimization)


pprint(method_info)
pprint(method_info2)


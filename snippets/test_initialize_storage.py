import logging
from pathlib import Path

from verity.storage.local import LocalStorage

logging.basicConfig(level=logging.DEBUG)

cwd = (Path(__file__) / "..").resolve()
target_dir = cwd / "storage"

st = LocalStorage(target_dir)
st.initialize()

prginfo = st.program_info()


ex_targets = list(st.execution_targets())


uid = st.experiment_run_uuid_get()
uid2 = st.optimization_report_uuid_get()
uid3 = st.execution_report_uuid_get()
uid4 = st.analysis_report_uuid_get()


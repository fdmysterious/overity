from pathlib import Path

from verity.exchange.inference_agent_package import package as agent_pkg
from pprint import pprint

from tempfile import TemporaryDirectory

from verity.storage.local import LocalStorage


cwd = Path(__file__).parent.resolve()
st = LocalStorage(cwd / "storage")
st.initialize()


#archive_path = cwd / "test_agent.tar.gz"

#meta = agent_pkg.metadata_load(archive_path)


print("######## AGENT METADATA")
meta = st.inference_agent_info_get("test_agent")
pprint(meta)

print("######## AGENT EXTRACT")
with TemporaryDirectory(delete=False) as tmpdir:
    print(f"Extract to {tmpdir}")

    meta = st.inference_agent_load("test_agent", tmpdir)
    pprint(meta)



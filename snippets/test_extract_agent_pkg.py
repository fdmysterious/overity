from pathlib import Path

from verity.exchange.inference_agent_package import package as agent_pkg
from pprint import pprint

from tempfile import TemporaryDirectory


cwd = Path(__file__).parent.resolve()

archive_path = cwd / "test_agent.tar.gz"

meta = agent_pkg.metadata_load(archive_path)


print("######## AGENT METADATA")
pprint(meta)
print()

print("######## AGENT EXTRACT")
with TemporaryDirectory(delete=False) as tmpdir:
    print(f"Extract to {tmpdir}")

    meta = agent_pkg.agent_load(archive_path, tmpdir)
    pprint(meta)



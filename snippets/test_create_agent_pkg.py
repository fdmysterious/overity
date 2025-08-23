from pathlib import Path

from verity.exchange.inference_agent_package import package as agent_pkg
from verity.model.inference_agent.metadata import InferenceAgentAuthor, InferenceAgentMaintainer, InferenceAgentMetadata
from verity.model.inference_agent.package import InferenceAgentPackageInfo

cwd = Path(__file__).parent

# Create agent metadata
agent_metadata = InferenceAgentMetadata(
    name="Test agent",
    version="0.1",
    authors = [
        InferenceAgentAuthor(name = "Florian Dupeyron", email = "florian.dupeyron@elsys-design.com", contribution="Initial design"),
    ],

    maintainers = [
        InferenceAgentAuthor(name = "Florian Dupeyron", email = "florian.dupeyron@elsys-design.com"),
    ],

    capabilities = frozenset({
        "measure-cpu-load",
        "measure-energy-consumption",
    }),

    compatible_targets = frozenset({
        "stm32g0xxx",
    }),

    compatible_tags = frozenset({
    })
)

agent_data_path = cwd / "resources" / "test_agent_data"

agent_pkginfo = InferenceAgentPackageInfo(
    metadata        = agent_metadata,
    agent_data_path = agent_data_path
)

archive_file_name = f"test_agent.tar.gz"

agent_pkg.package_archive_create(agent_pkginfo, cwd / archive_file_name)

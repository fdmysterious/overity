"""
Inference agent packaging tools

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- July 2025
"""

import tempfile
import tarfile
import hashlib

from pathlib import Path

from verity.model.inference_agent.package import InferenceAgentPackageInfo

from verity.exchange.inference_agent_package import metadata as agent_metadata


# TODO # Merge with one used in ml model package
def package_sha256(path: Path):
    path = Path(path)

    with open(path, "rb") as fhandle:
        digest = hashlib.file_digest(fhandle, "sha256")

    return digest


def package_archive_create(agent_data: InferenceAgentPackageInfo, output_path: Path):
    output_path = Path(output_path)

    with tempfile.NamedTemporaryFile(delete_on_close=False) as fhandle:
        # Encode metadata to JSON temporary file
        fhandle.close()  # File will be reopened by exchange encoding
        agent_metadata.to_file(agent_data.metadata, fhandle.name)

        # Create output archive
        with tarfile.open(output_path, "w:gz") as archive:
            archive.add(fhandle.name, arcname="agent-metadata.json")
            archive.add(agent_data.agent_data_path, arcname="data")

    # -> fhandle file is removed automatically when exiting the with... clause
    return package_sha256(output_path)

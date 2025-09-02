"""
Inference agent packaging tools
===============================

**July 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

import tempfile
import tarfile
import hashlib
import json

from pathlib import Path

from overity.model.inference_agent.metadata import InferenceAgentMetadata
from overity.model.inference_agent.package import InferenceAgentPackageInfo

from overity.exchange.inference_agent_package import metadata as agent_metadata

from overity.errors import MalformedAgentPackage


####################################################
# Create package
####################################################


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


####################################################
# Open package
####################################################


def _process_metadata(archive_path: Path, tf: tarfile.TarFile):
    """Utility function to load metadata from archive file"""

    info_json = tf.getmember("agent-metadata.json")

    if info_json is None:
        raise MalformedAgentPackage(archive_path, "No agent-metadata.json file")

    with tf.extractfile(info_json) as fhandle:
        data = json.load(fhandle)

    return agent_metadata.from_dict(data)


def _process_agent_data(archive_path: Path, tf: tarfile.TarFile, target_folder: Path):
    """Utility function to extract agent data from package archive"""

    data_folder = tf.getmember("data")

    if data_folder is None:
        raise MalformedAgentPackage(archive_path, "No data/ folder in package")

    # List of files in data folder
    data_files = filter(lambda x: x.name.startswith("data/"), tf.getmembers())

    tf.extractall(
        target_folder,
        members=list(
            data_files,
        ),
        filter="data",
    )


def metadata_load(archive_path: Path) -> InferenceAgentMetadata:
    """Load only agent metadata from archive path"""

    archive_path = Path(archive_path)

    with tarfile.open(archive_path, "r:gz") as archive:
        meta = _process_metadata(archive_path, archive)

    return meta


def agent_load(archive_path: Path, target_folder: Path) -> InferenceAgentPackageInfo:
    """Load agent metadata from archive, and extract its data to target folder"""

    archive_path = Path(archive_path)
    target_folder = Path(target_folder)

    with tarfile.open(archive_path, "r:gz") as archive:
        meta = _process_metadata(archive_path, archive)
        _process_agent_data(archive_path, archive, target_folder)

    return meta

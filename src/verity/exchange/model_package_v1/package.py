"""
# ML Model packaging tools

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- December 2024
"""

import tempfile
import tarfile

from pathlib import Path
from verity.model.ml_model.package import MLModelPackage

from . import metadata


def package_archive_create(model_data: MLModelPackage, output_path: Path):
    output_path = Path(output_path)

    with tempfile.NamedTemporaryFile(delete_on_close=False) as fhandle:
        # Encode metadata to JSON temporary file
        fhandle.close() # File will be reopened by exchange encoding
        metadata.to_file(model_data.metadata, fhandle.name)

        # Create output archive
        with tarfile.open(output_path, "w:gz") as archive:
            archive.add(fhandle.name, arcname="model-metadata.json")
            archive.add(model_data.model_file_path, arcname=model_data.metadata.model_file)

            if model_data.example_implementation_path is not None:
                archive.add(model_data.example_implementation_path, "inference-example")

    # -> fhandle is now removed

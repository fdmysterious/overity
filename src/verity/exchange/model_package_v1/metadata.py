"""
# Model metadata file encoder/decoder

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- December 2024
"""

import json
from pathlib import Path
from typing import Dict

from verity.model.ml_model.metadata import (
    MLModelAuthor,
    MLModelMaintainer,
    MLModelMetadata,
)

####################################################
# Decoder
####################################################


def _metadata_decode_model_author(data: Dict[str, any]):
    name = data["name"]
    email = data["email"]
    contribution = data.get("contribution")

    return MLModelAuthor(name=name, email=email, contribution=contribution)


def _metadata_decode_model_maintainer(data: Dict[str, any]):
    name = data["name"]
    email = data["email"]

    return MLModelMaintainer(name=name, email=email)


def _metadata_decode(data: Dict[str, any]):
    name = data["name"]
    version = data["version"]
    authors = [_metadata_decode_model_author(x) for x in data["authors"]]
    maintainers = [_metadata_decode_model_maintainer(x) for x in data["maintainers"]]
    target = data["target"]
    exchange_format = data["format"]
    model_file = data["model_file"]
    derives = data.get("derives")

    return MLModelMetadata(
        name=name,
        version=version,
        authors=authors,
        maintainers=maintainers,
        target=target,
        exchange_format=exchange_format,
        model_file=model_file,
        derives=derives,
    )


def from_file(json_path: Path):
    json_path = Path(json_path)

    # Parse JSON data
    with open(json_path) as fhandle:
        data = json.load(fhandle)

    # Validate file schema
    # TODO

    # Process elements
    return _metadata_decode(data)


####################################################
# Encoder
####################################################


def _metadata_encode_model_author(author: MLModelAuthor):
    encode_obj = {
        "name": author.name,
        "email": author.email,
    }

    if author.contribution is not None:
        encode_obj["contribution"] = author.contribution

    return encode_obj


def _metadata_encode_model_maintainer(maintainer: MLModelMaintainer):
    return {
        "name": maintainer.name,
        "email": maintainer.email,
    }


def _metadata_encode(metadata: MLModelMetadata):
    encode_obj = {
        "name": metadata.name,
        "version": metadata.version,
        "authors": [_metadata_encode_model_author(x) for x in metadata.authors],
        "maintainers": [
            _metadata_encode_model_maintainer(x) for x in metadata.maintainers
        ],
        "target": metadata.target,
        "format": metadata.exchange_format,
        "model_file": metadata.model_file,
    }

    if metadata.derives is not None:
        encode_obj["derives"] = metadata.derives

    return encode_obj


def to_file(metadata: MLModelMetadata, json_path: Path):
    json_path = Path(json_path)  # Ensure path is in correct type

    with open(json_path, "w") as fhandle:
        json.dump(_metadata_encode(metadata), fhandle)

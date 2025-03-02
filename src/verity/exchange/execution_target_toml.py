"""
# Execution target storage in TOML format

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

import jsonschema
import toml

from typing  import Dict, FrozenSet
from pathlib import Path

from verity.model.general_info.execution_target import ExecutionTarget


####################################################
# Validation schema
####################################################

SCHEMA = {
    "type": "object",
    "properties": {
        "target": {
            "type": "object",
            "properties": {
                # TODO # Slug is deduced for toml file name in local storage mode

                "name": {
                    "type": "string"
                },

                "description": {
                    "type": "string"
                },

                "tags": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            },

            "required": [
                "name",
            ]
        }
    },

    "required": ["target"],
}


####################################################
# Decoder
####################################################

def _execution_target_decode(slug: str, data: Dict[str, any]):
    target_info = data["target"]

    return ExecutionTarget(
        slug         = slug,
        display_name = target_info["name"],
        description  = target_info.get("description", None),
        tags         = target_info.get("tags", None)
    )

def from_file(toml_path: Path):
    """Decode the given file containing execution target information"""

    toml_path = Path(toml_path)

    # Parse TOML data
    with open(toml_path, "r") as fhandle:
        data = toml.load(fhandle)


    # Validate data
    jsonschema.validate(data, SCHEMA)


    # Get slug from file name
    slug = toml_path.stem


    # Parse information
    extg = _execution_target_decode(slug, data)

    return extg



####################################################
# Encoder
####################################################

# TODO #

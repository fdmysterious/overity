"""
# Program information storage in TOML format

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

import jsonschema
import toml

from typing import Dict
from datetime import date
from pathlib import Path

from verity.model.general_info.program import ProgramInitiator, ProgramInfo



####################################################
# Validation schema
####################################################

SCHEMA = {
  "type": "object",
  "properties": {
    "program": {
      "type": "object",
      "properties": {
        "slug": {
          "type": "string"
        },
        "display_name": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "date_created": {
          "type": "string",
          "format": "date-time"
        },
        "active": {
          "type": "boolean"
        }
      },
      "required": ["slug", "display_name", "date_created", "active"]
    },

    "initiator": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "email": {
          "type": "string",
          "format": "email"
        },
        "role": {
          "type": "string"
        }
      },
      "required": ["name", "email"]
    }
  },
  "required": ["program", "initiator"]
}


####################################################
# Decoder
####################################################

def _program_decode_initiator(data: Dict[str, any]):
    return ProgramInitiator(
        name  = data["name"],
        email = data["email"],
        role  = data.get("role")
    )


def _program_decode(data: Dict[str, any]):
    program_info   = data["program"  ]
    initiator_info = data["initiator"]

    initiator = _program_decode_initiator(initiator_info)
    program   = ProgramInfo(
        slug = program_info["slug"],
        display_name = program_info["display_name"],
        description = program_info.get("description"),
        date_created = date.fromisoformat(program_info["date_created"]),
        initiator = initiator,
    )

    return program


def from_file(toml_path: Path):
    """Decode the given file containing program information"""

    # Parse TOML data
    with open(toml_path, "r") as fhandle:
        data = toml.load(fhandle)


    # Validate data
    jsonschema.validate(data, SCHEMA)

    # Parse information
    program = _program_decode(data)

    return program


####################################################
# Encoder
####################################################

# TODO #

"""
Inference agent package model

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- June 2025
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from verity.model.inference_agent.metadata import InferenceAgentMetadata


@dataclass
class InferenceAgentPackage:
    """Describes properties for an inference agent package"""

    """Inference agent metadata information"""
    metadata: InferenceAgentMetadata

    """Path to inference agent artefact on local disk"""
    inference_agent_path: Path

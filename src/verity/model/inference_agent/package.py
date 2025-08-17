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
class InferenceAgentPackageInfo:
    """Describes what is needed to build an inference agent package"""

    """Inference agent metadata information"""
    metadata: InferenceAgentMetadata

    """Path to inference agent data on local disk"""
    agent_data_path: Path

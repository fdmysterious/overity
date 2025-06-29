"""
Inference agent metadata model

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- June 2025
"""

from __future__ import annotations

from dataclasses import dataclass

from verity.model.general_info.capability import Capability


@dataclass
class InferenceAgentAuthor:
    """Describes an author entry for an inference agent metadata"""

    """Name of the author"""
    name: str

    """Email address of the author"""
    email: str

    """Optional string describing what its contribution was to the program"""
    contribution: str | None = None


@dataclass
class InferenceAgentMaintainer:
    """Describes a maintainer entry for inference agent"""

    """Name of the maintainer"""
    name: str

    """Email of the maintainer"""
    email: str


@dataclass
class InferenceAgentMetadata:
    """Describes the properties of an inference agent"""

    """Name of the inference agent"""
    name: str

    """Version of the inference agent"""
    version: str

    """List of authors"""
    authors: list[InferenceAgentAuthor]

    """List of maintainers"""
    maintainers: list[InferenceAgentMaintainer]

    """List of capabilities for the inference agent"""
    capabilities: frozenset[Capability]

    """List of compatible execution targets"""
    compatible_targets: frozenset[str]

    """List of compatible tags"""
    compatible_tags: frozenset[str]

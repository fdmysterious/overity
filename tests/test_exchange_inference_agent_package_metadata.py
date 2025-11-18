"""
Unit tests for inference_agent_package/metadata.py
"""

import pytest
import tempfile
import json
from pathlib import Path
from overity.exchange.inference_agent_package.metadata import (
    from_file,
    to_file,
    from_dict,
)
from overity.model.inference_agent.metadata import (
    InferenceAgentMetadata,
    InferenceAgentAuthor,
    InferenceAgentMaintainer,
)


class TestInferenceAgentPackageMetadata:
    def test_valid_inference_agent_metadata(self):
        """Test parsing a valid inference agent metadata JSON file."""
        data = {
            "name": "Test Inference Agent",
            "version": "1.0.0",
            "authors": [
                {"name": "John Doe", "email": "john@example.com"},
                {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "contribution": "Core algorithm",
                },
            ],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
            "capabilities": ["text-generation", "summarization"],
            "compatible_targets": ["cpu", "gpu"],
            "compatible_tags": ["latest", "stable"],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, InferenceAgentMetadata)
                assert result.name == "Test Inference Agent"
                assert result.version == "1.0.0"
                assert result.capabilities == frozenset(
                    ["text-generation", "summarization"]
                )
                assert result.compatible_targets == frozenset(["cpu", "gpu"])
                assert result.compatible_tags == frozenset(["latest", "stable"])

                assert len(result.authors) == 2
                assert isinstance(result.authors[0], InferenceAgentAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert isinstance(result.authors[1], InferenceAgentAuthor)
                assert result.authors[1].name == "Jane Smith"
                assert result.authors[1].email == "jane@example.com"
                assert result.authors[1].contribution == "Core algorithm"

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], InferenceAgentMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_minimal_inference_agent_metadata(self):
        """Test parsing a minimal inference agent metadata JSON file."""
        data = {
            "name": "Minimal Inference Agent",
            "version": "1.0.0",
            "authors": [{"name": "John Doe", "email": "john@example.com"}],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
            "capabilities": [],
            "compatible_targets": [],
            "compatible_tags": [],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, InferenceAgentMetadata)
                assert result.name == "Minimal Inference Agent"
                assert result.version == "1.0.0"
                assert result.capabilities == frozenset()
                assert result.compatible_targets == frozenset()
                assert result.compatible_tags == frozenset()

                assert len(result.authors) == 1
                assert isinstance(result.authors[0], InferenceAgentAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], InferenceAgentMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_round_trip_inference_agent_metadata(self):
        """Test that encoding and decoding an InferenceAgentMetadata works correctly."""
        original = InferenceAgentMetadata(
            name="Round Trip Inference Agent",
            version="2.0.0",
            authors=[
                InferenceAgentAuthor(
                    name="John Doe", email="john@example.com", contribution=None
                ),
                InferenceAgentAuthor(
                    name="Jane Smith",
                    email="jane@example.com",
                    contribution="Core algorithm",
                ),
            ],
            maintainers=[
                InferenceAgentMaintainer(
                    name="Maintainer One", email="maintainer1@example.com"
                )
            ],
            capabilities=frozenset(["text-generation", "summarization"]),
            compatible_targets=frozenset(["cpu", "gpu"]),
            compatible_tags=frozenset(["latest", "stable"]),
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Encode to file
            to_file(original, temp_path)

            # Decode from file
            result = from_file(temp_path)

            # Assertions
            assert result.name == original.name
            assert result.version == original.version
            assert result.capabilities == original.capabilities
            assert result.compatible_targets == original.compatible_targets
            assert result.compatible_tags == original.compatible_tags

            assert len(result.authors) == len(original.authors)
            for i in range(len(result.authors)):
                assert result.authors[i].name == original.authors[i].name
                assert result.authors[i].email == original.authors[i].email
                assert (
                    result.authors[i].contribution == original.authors[i].contribution
                )

            assert len(result.maintainers) == len(original.maintainers)
            for i in range(len(result.maintainers)):
                assert result.maintainers[i].name == original.maintainers[i].name
                assert result.maintainers[i].email == original.maintainers[i].email
        finally:
            temp_path.unlink()

    def test_from_dict_function(self):
        """Test the from_dict function directly."""
        data = {
            "name": "Dict Test Agent",
            "version": "1.5.0",
            "authors": [{"name": "Test Author", "email": "test@example.com"}],
            "maintainers": [{"name": "Test Maintainer", "email": "maint@example.com"}],
            "capabilities": ["test-capability"],
            "compatible_targets": ["test-target"],
            "compatible_tags": ["test-tag"],
        }

        result = from_dict(data)
        assert isinstance(result, InferenceAgentMetadata)
        assert result.name == "Dict Test Agent"
        assert result.version == "1.5.0"
        assert result.capabilities == frozenset(["test-capability"])
        assert result.compatible_targets == frozenset(["test-target"])
        assert result.compatible_tags == frozenset(["test-tag"])

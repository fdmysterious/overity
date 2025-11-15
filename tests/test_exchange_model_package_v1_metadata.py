"""
Unit tests for model_package_v1/metadata.py
"""

import pytest
import tempfile
import json
from pathlib import Path
from overity.exchange.model_package_v1.metadata import from_file, to_file
from overity.model.ml_model.metadata import (
    MLModelMetadata,
    MLModelAuthor,
    MLModelMaintainer,
)


class TestModelPackageV1Metadata:
    def test_valid_model_metadata(self):
        """Test parsing a valid model metadata JSON file."""
        data = {
            "name": "Test Model",
            "version": "1.0.0",
            "authors": [
                {"name": "John Doe", "email": "john@example.com"},
                {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "contribution": "Model architecture",
                },
            ],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
            "target": "test-target",
            "format": "onnx",
            "model_file": "model.onnx",
            "derives": "base-model",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, MLModelMetadata)
                assert result.name == "Test Model"
                assert result.version == "1.0.0"
                assert result.target == "test-target"
                assert result.exchange_format == "onnx"
                assert result.model_file == "model.onnx"
                assert result.derives == "base-model"

                assert len(result.authors) == 2
                assert isinstance(result.authors[0], MLModelAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert isinstance(result.authors[1], MLModelAuthor)
                assert result.authors[1].name == "Jane Smith"
                assert result.authors[1].email == "jane@example.com"
                assert result.authors[1].contribution == "Model architecture"

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], MLModelMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_minimal_model_metadata(self):
        """Test parsing a minimal model metadata JSON file."""
        data = {
            "name": "Minimal Model",
            "version": "1.0.0",
            "authors": [{"name": "John Doe", "email": "john@example.com"}],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
            "target": "minimal-target",
            "format": "onnx",
            "model_file": "model.onnx",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, MLModelMetadata)
                assert result.name == "Minimal Model"
                assert result.version == "1.0.0"
                assert result.target == "minimal-target"
                assert result.exchange_format == "onnx"
                assert result.model_file == "model.onnx"
                assert result.derives is None

                assert len(result.authors) == 1
                assert isinstance(result.authors[0], MLModelAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], MLModelMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_round_trip_model_metadata(self):
        """Test that encoding and decoding a MLModelMetadata works correctly."""
        original = MLModelMetadata(
            name="Round Trip Model",
            version="2.0.0",
            authors=[
                MLModelAuthor(
                    name="John Doe", email="john@example.com", contribution=None
                ),
                MLModelAuthor(
                    name="Jane Smith",
                    email="jane@example.com",
                    contribution="Model architecture",
                ),
            ],
            maintainers=[
                MLModelMaintainer(
                    name="Maintainer One", email="maintainer1@example.com"
                )
            ],
            target="round-trip-target",
            exchange_format="onnx",
            model_file="model.onnx",
            derives="base-model",
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
            assert result.target == original.target
            assert result.exchange_format == original.exchange_format
            assert result.model_file == original.model_file
            assert result.derives == original.derives

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

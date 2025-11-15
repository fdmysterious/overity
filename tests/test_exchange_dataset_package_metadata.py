"""
Unit tests for dataset_package/metadata.py
"""

import pytest
import tempfile
import json
from pathlib import Path
from overity.exchange.dataset_package.metadata import from_file, to_file
from overity.model.dataset.metadata import (
    DatasetMetadata,
    DatasetAuthor,
    DatasetMaintainer,
)


class TestDatasetPackageMetadata:
    def test_valid_dataset_metadata(self):
        """Test parsing a valid dataset metadata JSON file."""
        data = {
            "name": "Test Dataset",
            "authors": [
                {"name": "John Doe", "email": "john@example.com"},
                {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "contribution": "Data collection",
                },
            ],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
            "description": "A test dataset",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, DatasetMetadata)
                assert result.name == "Test Dataset"
                assert result.description == "A test dataset"

                assert len(result.authors) == 2
                assert isinstance(result.authors[0], DatasetAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert isinstance(result.authors[1], DatasetAuthor)
                assert result.authors[1].name == "Jane Smith"
                assert result.authors[1].email == "jane@example.com"
                assert result.authors[1].contribution == "Data collection"

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], DatasetMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_minimal_dataset_metadata(self):
        """Test parsing a minimal dataset metadata JSON file."""
        data = {
            "name": "Minimal Dataset",
            "authors": [{"name": "John Doe", "email": "john@example.com"}],
            "maintainers": [
                {"name": "Maintainer One", "email": "maintainer1@example.com"}
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, DatasetMetadata)
                assert result.name == "Minimal Dataset"
                assert result.description is None

                assert len(result.authors) == 1
                assert isinstance(result.authors[0], DatasetAuthor)
                assert result.authors[0].name == "John Doe"
                assert result.authors[0].email == "john@example.com"
                assert result.authors[0].contribution is None

                assert len(result.maintainers) == 1
                assert isinstance(result.maintainers[0], DatasetMaintainer)
                assert result.maintainers[0].name == "Maintainer One"
                assert result.maintainers[0].email == "maintainer1@example.com"
            finally:
                Path(f.name).unlink()

    def test_round_trip_dataset_metadata(self):
        """Test that encoding and decoding a DatasetMetadata works correctly."""
        original = DatasetMetadata(
            name="Round Trip Dataset",
            authors=[
                DatasetAuthor(
                    name="John Doe", email="john@example.com", contribution=None
                ),
                DatasetAuthor(
                    name="Jane Smith",
                    email="jane@example.com",
                    contribution="Data collection",
                ),
            ],
            maintainers=[
                DatasetMaintainer(
                    name="Maintainer One", email="maintainer1@example.com"
                )
            ],
            description="Testing round trip",
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
            assert result.description == original.description

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

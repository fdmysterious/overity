"""
Unit tests for capability_toml.py
"""

import pytest
import tempfile
import toml
from pathlib import Path
from jsonschema import ValidationError
from overity.exchange.capability_toml import from_file
from overity.model.general_info.capability import Capability


class TestCapabilityToml:
    def test_valid_capability_toml(self):
        """Test parsing a valid capability TOML file."""
        data = {
            "capability": {
                "name": "Test Capability",
                "description": "A test capability",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, Capability)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Test Capability"
                assert result.description == "A test capability"
            finally:
                Path(f.name).unlink()

    def test_minimal_capability_toml(self):
        """Test parsing a minimal capability TOML file with only required fields."""
        data = {
            "capability": {
                "name": "Minimal Capability",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, Capability)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Minimal Capability"
                assert result.description is None
            finally:
                Path(f.name).unlink()

    def test_invalid_capability_toml_missing_required(self):
        """Test that parsing fails for TOML missing required fields."""
        data = {
            "capability": {
                "description": "Invalid Capability"
                # Missing required field: name
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

    def test_invalid_capability_toml_wrong_structure(self):
        """Test that parsing fails for TOML with wrong structure."""
        data = {"not_capability": {"name": "wrong-structure"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

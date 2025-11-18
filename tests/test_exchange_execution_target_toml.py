"""
Unit tests for execution_target_toml.py
"""

import pytest
import tempfile
import toml
from pathlib import Path
from jsonschema import ValidationError
from overity.exchange.execution_target_toml import from_file
from overity.model.general_info.execution_target import ExecutionTarget


class TestExecutionTargetToml:
    def test_valid_execution_target_toml(self):
        """Test parsing a valid execution target TOML file."""
        data = {
            "target": {
                "name": "Test Target",
                "description": "A test target",
                "tags": ["tag1", "tag2", "tag3"],
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, ExecutionTarget)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Test Target"
                assert result.description == "A test target"
                assert set(result.tags) == {"tag1", "tag2", "tag3"}
            finally:
                Path(f.name).unlink()

    def test_minimal_execution_target_toml(self):
        """Test parsing a minimal execution target TOML file with only required fields."""
        data = {
            "target": {
                "name": "Minimal Target",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, ExecutionTarget)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Minimal Target"
                assert result.description is None
                assert result.tags is None
            finally:
                Path(f.name).unlink()

    def test_invalid_execution_target_toml_missing_required(self):
        """Test that parsing fails for TOML missing required fields."""
        data = {
            "target": {
                "description": "Invalid Target"
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

    def test_invalid_execution_target_toml_wrong_structure(self):
        """Test that parsing fails for TOML with wrong structure."""
        data = {"not_target": {"name": "wrong-structure"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

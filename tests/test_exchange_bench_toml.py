"""
Unit tests for bench_toml.py
"""

import pytest
import tempfile
import toml
from pathlib import Path
from jsonschema import ValidationError
from overity.exchange.bench_toml import from_file
from overity.model.general_info.bench import BenchInstanciationMetadata


class TestBenchToml:
    def test_valid_bench_toml(self):
        """Test parsing a valid bench TOML file."""
        data = {
            "bench": {
                "name": "Test Bench",
                "description": "A test bench",
                "abstraction": "test-abstraction",
                "settings": {
                    "param1": "value1",
                    "param2": 42,
                    "param3": True,
                    "param4": 3.14,
                },
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, BenchInstanciationMetadata)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Test Bench"
                assert result.abstraction_slug == "test-abstraction"
                assert result.description == "A test bench"
                assert result.settings == {
                    "param1": "value1",
                    "param2": 42,
                    "param3": True,
                    "param4": 3.14,
                }
            finally:
                Path(f.name).unlink()

    def test_minimal_bench_toml(self):
        """Test parsing a minimal bench TOML file with only required fields."""
        data = {
            "bench": {
                "name": "Minimal Bench",
                "abstraction": "minimal-abstraction",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, BenchInstanciationMetadata)
                assert result.slug == Path(f.name).stem  # Slug deduced from filename
                assert result.display_name == "Minimal Bench"
                assert result.abstraction_slug == "minimal-abstraction"
                assert result.description is None
                assert result.settings is None
            finally:
                Path(f.name).unlink()

    def test_invalid_bench_toml_missing_required(self):
        """Test that parsing fails for TOML missing required fields."""
        data = {
            "bench": {
                "name": "Invalid Bench"
                # Missing required field: abstraction
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

    def test_invalid_bench_toml_wrong_structure(self):
        """Test that parsing fails for TOML with wrong structure."""
        data = {"not_bench": {"name": "wrong-structure"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

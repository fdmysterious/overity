"""
Unit tests for program_toml.py
"""

import pytest
import tempfile
import toml
from pathlib import Path
from datetime import date
import jsonschema

from overity.exchange.program_toml import from_file, to_file
from overity.model.general_info.program import ProgramInfo, ProgramInitiator


class TestProgramToml:
    def test_valid_program_toml(self):
        """Test parsing a valid program TOML file."""
        data = {
            "program": {
                "slug": "test-program",
                "display_name": "Test Program",
                "description": "A test program",
                "date_created": "2023-01-01",
                "active": True,
            },
            "initiator": {
                "name": "John Doe",
                "email": "john@example.com",
                "role": "Developer",
            },
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, ProgramInfo)
                assert result.slug == "test-program"
                assert result.display_name == "Test Program"
                assert result.description == "A test program"
                assert result.date_created == date(2023, 1, 1)
                assert result.active is True
                assert isinstance(result.initiator, ProgramInitiator)
                assert result.initiator.name == "John Doe"
                assert result.initiator.email == "john@example.com"
                assert result.initiator.role == "Developer"
            finally:
                Path(f.name).unlink()

    def test_minimal_program_toml(self):
        """Test parsing a minimal program TOML file with only required fields."""
        data = {
            "program": {
                "slug": "minimal-program",
                "display_name": "Minimal Program",
                "date_created": "2023-01-01",
                "active": False,
            },
            "initiator": {"name": "Jane Doe", "email": "jane@example.com"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                result = from_file(Path(f.name))
                assert isinstance(result, ProgramInfo)
                assert result.slug == "minimal-program"
                assert result.display_name == "Minimal Program"
                assert result.description is None
                assert result.date_created == date(2023, 1, 1)
                assert result.active is False
                assert isinstance(result.initiator, ProgramInitiator)
                assert result.initiator.name == "Jane Doe"
                assert result.initiator.email == "jane@example.com"
                assert result.initiator.role is None
            finally:
                Path(f.name).unlink()

    def test_invalid_program_toml_missing_required(self):
        """Test that parsing fails for TOML missing required fields."""
        data = {
            "program": {
                "display_name": "Invalid Program"
                # Missing required fields: slug, date_created, active
            },
            "initiator": {"name": "John Doe", "email": "john@example.com"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(jsonschema.ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

    def test_invalid_program_toml_wrong_structure(self):
        """Test that parsing fails for TOML with wrong structure."""
        data = {"not_program": {"slug": "wrong-structure"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            toml.dump(data, f)
            f.flush()

            try:
                with pytest.raises(jsonschema.ValidationError):
                    from_file(Path(f.name))
            finally:
                Path(f.name).unlink()

    def test_round_trip_program_toml(self):
        """Test that encoding and decoding a ProgramInfo works correctly."""
        original = ProgramInfo(
            slug="round-trip-program",
            display_name="Round Trip Program",
            description="Testing round trip",
            date_created=date(2023, 6, 15),
            initiator=ProgramInitiator(
                name="Test User", email="test@example.com", role="Tester"
            ),
            active=True,
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            temp_path = Path(f.name)

        try:
            to_file(original, temp_path)
            result = from_file(temp_path)

            assert result.slug == original.slug
            assert result.display_name == original.display_name
            assert result.description == original.description
            assert result.date_created == original.date_created
            assert result.active == original.active
            assert result.initiator.name == original.initiator.name
            assert result.initiator.email == original.initiator.email
            assert result.initiator.role == original.initiator.role
        finally:
            temp_path.unlink()

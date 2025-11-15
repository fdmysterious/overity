"""
Unit tests for bench_abstraction/file_py.py
"""

import pytest
import tempfile
from pathlib import Path
from textwrap import dedent
from overity.exchange.bench_abstraction.file_py import from_file, import_definitions
from overity.errors import EmptyMethodDescription


class TestBenchAbstractionFilePy:
    def test_from_file_valid(self):
        """Test parsing a valid bench abstraction python file."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(
                dedent("""
                \"\"\"
                # Test Bench

                **field1**: value1

                - John Doe (john@example.com)

                Some description text here.
                \"\"\"
                
                from dataclasses import dataclass
                
                @dataclass
                class BenchSettings:
                    pass
                    
                class BenchDefinition:
                    pass
            """).encode()
            )
            f.flush()

            path = Path(f.name)

        result = from_file(path)

        assert result.slug == path.name.removesuffix(".py")
        assert result.display_name == "Test Bench"
        assert result.description.strip() == "Some description text here."
        assert result.metadata == {"field1": "value1"}

        assert len(result.authors) == 1
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"

    def test_from_file_empty_docstring(self):
        """Test that parsing fails for bench abstraction with empty docstring."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(
                dedent("""
                from dataclasses import dataclass
                
                @dataclass
                class BenchSettings:
                    pass
                    
                class BenchDefinition:
                    pass
            """).encode()
            )
            f.flush()

            path = Path(f.name)

        with pytest.raises(EmptyMethodDescription):
            from_file(path)

    def test_import_definitions_valid(self):
        """Test importing bench abstraction definitions from a valid python file."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(
                dedent("""
                from dataclasses import dataclass
                
                @dataclass
                class BenchSettings:
                    field: str = "test"
                    
                class BenchDefinition:
                    def __init__(self):
                        self.value = "test"
            """).encode()
            )
            f.flush()

            path = Path(f.name)

        BenchSettings, BenchDefinition = import_definitions(path)

        assert BenchSettings.__name__ == "BenchSettings"
        assert BenchDefinition.__name__ == "BenchDefinition"

        # Test instantiation
        settings = BenchSettings()
        assert settings.field == "test"

        definition = BenchDefinition()
        assert definition.value == "test"

    def test_import_definitions_missing_classes(self):
        """Test that importing fails when required classes are missing."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(
                dedent("""
                from dataclasses import dataclass
                
                @dataclass
                class BenchSettings:
                    field: str = "test"
            """).encode()
            )
            f.flush()

            path = Path(f.name)

        with pytest.raises(AttributeError):
            import_definitions(path)

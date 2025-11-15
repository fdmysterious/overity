"""
Unit tests for bench_abstraction/description_md.py
"""

import pytest
from pathlib import Path
from textwrap import dedent
from parsimonious.exceptions import ParseError
from overity.exchange.bench_abstraction.description_md import from_md_desc
from overity.model.general_info.bench import (
    BenchAbstractionMetadata,
    BenchAbstractionAuthor,
)


class TestBenchAbstractionDescriptionMd:
    def test_valid_bench_description_hash_title(self):
        """Test parsing a valid bench description with hash title."""

        md_content = dedent("""
            # Test Bench

            **field1**: value1

            **field2**: value2

            - John Doe (john@example.com)
            - Jane Smith (jane@example.com) : Lead developer

            Some description text here.
            """).strip()

        result = from_md_desc("test-bench", md_content, Path("/test/path"))

        assert isinstance(result, BenchAbstractionMetadata)
        assert result.slug == "test-bench"
        assert result.display_name == "Test Bench"
        assert result.description.strip() == "Some description text here."
        assert result.metadata == {"field1": "value1", "field2": "value2"}

        assert len(result.authors) == 2
        assert isinstance(result.authors[0], BenchAbstractionAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"
        assert result.authors[0].contribution is None

        assert isinstance(result.authors[1], BenchAbstractionAuthor)
        assert result.authors[1].name == "Jane Smith"
        assert result.authors[1].email == "jane@example.com"
        assert result.authors[1].contribution == "Lead developer"

    def test_valid_bench_description_underline_title(self):
        """Test parsing a valid bench description with underline title."""

        md_content = dedent("""
            Test Bench
            ==========

            **field1**: value1

            - John Doe (john@example.com)

            Some description text here.
            """).strip()

        result = from_md_desc("test-bench", md_content, Path("/test/path"))

        assert isinstance(result, BenchAbstractionMetadata)
        assert result.slug == "test-bench"
        assert result.display_name == "Test Bench"
        assert result.description.strip() == "Some description text here."
        assert result.metadata == {"field1": "value1"}

        assert len(result.authors) == 1
        assert isinstance(result.authors[0], BenchAbstractionAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"

    def test_minimal_bench_description(self):
        """Test parsing a minimal bench description."""

        md_content = dedent("""
        # Minimal Bench

        - John Doe (john@example.com)
        """).strip()

        result = from_md_desc("minimal-bench", md_content, Path("/test/path"))

        assert isinstance(result, BenchAbstractionMetadata)
        assert result.slug == "minimal-bench"
        assert result.display_name == "Minimal Bench"
        assert result.description.strip() == ""
        assert result.metadata == {}

        assert len(result.authors) == 1
        assert isinstance(result.authors[0], BenchAbstractionAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"

    def test_invalid_bench_description_no_authors(self):
        """Test that parsing fails for bench description with no authors."""

        md_content = dedent("""
        # Invalid Bench

        No authors here.
        """).strip()

        # This should fail because the grammar expects at least one author
        with pytest.raises(ParseError):
            from_md_desc("invalid-bench", md_content, Path("/test/path"))

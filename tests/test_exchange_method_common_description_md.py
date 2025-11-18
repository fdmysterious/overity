"""
Unit tests for method_common/description_md.py
"""

import pytest
from pathlib import Path
from textwrap import dedent
from parsimonious.exceptions import ParseError
from overity.exchange.method_common.description_md import from_md_desc
from overity.model.general_info.method import MethodInfo, MethodAuthor, MethodKind


class TestMethodCommonDescriptionMd:
    def test_valid_method_description_hash_title(self):
        """Test parsing a valid method description with hash title."""
        md_content = dedent(
            """
            # Test Method

            **field1**: value1

            **field2**: value2

            - John Doe (john@example.com)
            - Jane Smith (jane@example.com) : Lead developer

            Some description text here.
            """
        ).strip()

        result = from_md_desc(
            "test-method",
            MethodKind.TrainingOptimization,
            md_content,
            Path("/test/path"),
        )

        assert isinstance(result, MethodInfo)
        assert result.slug == "test-method"
        assert result.kind == MethodKind.TrainingOptimization
        assert result.display_name == "Test Method"
        assert result.description.strip() == "Some description text here."
        assert result.metadata == {"field1": "value1", "field2": "value2"}
        assert result.path == Path("/test/path")

        assert len(result.authors) == 2
        assert isinstance(result.authors[0], MethodAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"
        assert result.authors[0].contribution is None

        assert isinstance(result.authors[1], MethodAuthor)
        assert result.authors[1].name == "Jane Smith"
        assert result.authors[1].email == "jane@example.com"
        assert result.authors[1].contribution == "Lead developer"

    def test_valid_method_description_underline_title(self):
        """Test parsing a valid method description with underline title."""

        md_content = dedent(
            """
            Test Method
            ===========

            **field1**: value1

            - John Doe (john@example.com)

            Some description text here.
            """
        ).strip()

        result = from_md_desc(
            "test-method",
            MethodKind.TrainingOptimization,
            md_content,
            Path("/test/path"),
        )

        assert isinstance(result, MethodInfo)
        assert result.slug == "test-method"
        assert result.kind == MethodKind.TrainingOptimization
        assert result.display_name == "Test Method"
        assert result.description.strip() == "Some description text here."
        assert result.metadata == {"field1": "value1"}
        assert result.path == Path("/test/path")

        assert len(result.authors) == 1
        assert isinstance(result.authors[0], MethodAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"


    def test_minimal_method_description(self):
        """Test parsing a minimal method description."""

        md_content = dedent(
            """
            # Minimal Method

            - John Doe (john@example.com)
            """
        ).strip()

        result = from_md_desc(
            "minimal-method",
            MethodKind.TrainingOptimization,
            md_content,
            Path("/test/path"),
        )

        assert isinstance(result, MethodInfo)
        assert result.slug == "minimal-method"
        assert result.kind == MethodKind.TrainingOptimization
        assert result.display_name == "Minimal Method"
        assert result.description.strip() == ""
        assert result.metadata == {}
        assert result.path == Path("/test/path")

        assert len(result.authors) == 1
        assert isinstance(result.authors[0], MethodAuthor)
        assert result.authors[0].name == "John Doe"
        assert result.authors[0].email == "john@example.com"


    def test_invalid_method_description_no_authors(self):
        """Test that parsing fails for method description with no authors."""

        md_content = dedent(
            """
            # Invalid Method

            No authors here.
            """
        ).strip()

        # This should fail because the grammar expects at least one author
        with pytest.raises(ParseError):
            from_md_desc(
                "invalid-method",
                MethodKind.TrainingOptimization,
                md_content,
                Path("/test/path"),
            )

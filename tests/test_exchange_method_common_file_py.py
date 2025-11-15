"""
Unit tests for method_common/file_py.py
"""

import pytest
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch, mock_open

from overity.exchange.method_common.file_py import (
    from_file,
    _extract_slug,
    _read_docstring,
)
from overity.model.general_info.method import MethodKind
from overity.errors import EmptyMethodDescription


class TestMethodCommonFilePy:
    def test_extract_slug(self):
        """Test extracting slug from path."""
        path = Path("/some/path/method_name.py")
        assert _extract_slug(path) == "method_name"

    def test_read_docstring_with_module_docstring(self):
        """Test reading docstring from a Python file with module docstring."""
        py_content = dedent(
            '''
            """
            # Test Method

            **field1**: value1

            - John Doe (john@example.com)

            Some description text here.
            """

            def some_function():
                pass
            '''
        )

        with patch("pathlib.Path.read_text", return_value=py_content):
            result = _read_docstring(Path("/test/path/method_name.py"))
            assert result is not None
            assert "# Test Method" in result

    def test_read_docstring_without_module_docstring(self):
        """Test reading docstring from a Python file without module docstring."""
        py_content = dedent(
            '''
            def some_function():
                """This is a function docstring."""
                pass
            '''
        )

        with patch("pathlib.Path.read_text", return_value=py_content):
            result = _read_docstring(Path("/test/path/method_name.py"))
            assert result is None

    def test_from_file_with_valid_docstring(self):
        """Test parsing method info from a valid Python file."""
        py_content = dedent(
            '''
            """
            # Test Method

            **field1**: value1

            - John Doe (john@example.com)

            Some description text here.
            """

            def some_function():
                pass
            '''
        )

        with patch("pathlib.Path.read_text", return_value=py_content):
            # Mock the from_md_desc function to avoid dependency on its implementation
            with patch(
                "overity.exchange.method_common.file_py.description_md.from_md_desc"
            ) as mock_from_md_desc:
                from_file(
                    Path("/test/path/method_name.py"), MethodKind.TrainingOptimization
                )
                mock_from_md_desc.assert_called_once()

    def test_from_file_without_docstring_raises_exception(self):
        """Test that parsing fails for a Python file without docstring."""
        py_content = dedent(
            """
            def some_function():
                pass
            """
        )

        with patch("pathlib.Path.read_text", return_value=py_content):
            with pytest.raises(EmptyMethodDescription):
                from_file(
                    Path("/test/path/method_name.py"), MethodKind.TrainingOptimization
                )

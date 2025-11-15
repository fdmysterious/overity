"""
Unit tests for method_common/file_ipynb.py
"""

import pytest
import json
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch, mock_open, MagicMock

import nbformat

from overity.exchange.method_common.file_ipynb import (
    from_file,
    _extract_slug,
    _extract_first_md_cell,
)
from overity.model.general_info.method import MethodKind, MethodInfo
from overity.errors import EmptyMethodDescription


class TestMethodCommonFileIpynb:
    def test_extract_slug(self):
        """Test extracting slug from path."""
        path = Path("/some/path/method_name.ipynb")
        assert _extract_slug(path) == "method_name"

    def test_extract_first_md_cell_with_markdown_cell(self):
        """Test extracting the first markdown cell from a notebook."""
        # Create a mock notebook structure
        nb = nbformat.v4.new_notebook()
        nb.cells = [
            nbformat.v4.new_code_cell("print('hello')"),
            nbformat.v4.new_markdown_cell("# Test Method\n\nSome description"),
            nbformat.v4.new_markdown_cell("# Another Cell"),
        ]

        with patch("nbformat.read", return_value=nb):
            with patch("builtins.open", mock_open()):
                result = _extract_first_md_cell(Path("/test/path/method_name.ipynb"))
                assert result["cell_type"] == "markdown"
                assert "# Test Method" in result["source"]

    def test_extract_first_md_cell_without_markdown_cell(self):
        """Test extracting markdown cell from a notebook with no markdown cells."""
        # Create a mock notebook structure with only code cells
        nb = nbformat.v4.new_notebook()
        nb.cells = [
            nbformat.v4.new_code_cell("print('hello')"),
            nbformat.v4.new_code_cell("x = 1"),
        ]

        with patch("nbformat.read", return_value=nb):
            with patch("builtins.open", mock_open()):
                with pytest.raises(StopIteration):
                    _extract_first_md_cell(Path("/test/path/method_name.ipynb"))

    def test_from_file_with_valid_markdown_cell(self):
        """Test parsing method info from a valid notebook file."""
        # Create a mock notebook structure
        nb = nbformat.v4.new_notebook()
        nb.cells = [
            nbformat.v4.new_code_cell("print('hello')"),
            nbformat.v4.new_markdown_cell(
                dedent("""
                # Test Method

                **field1**: value1

                - John Doe (john@example.com)

                Some description text here.
            """).strip()
            ),
        ]

        # Mock the return value of nbformat.read
        with patch("nbformat.read", return_value=nb):
            with patch("builtins.open", mock_open()):
                # Mock the from_md_desc function to avoid dependency on its implementation
                with patch(
                    "overity.exchange.method_common.file_ipynb.description_md.from_md_desc"
                ) as mock_from_md_desc:
                    # Create a mock MethodInfo to return
                    mock_method_info = MagicMock(spec=MethodInfo)
                    mock_from_md_desc.return_value = mock_method_info

                    result = from_file(
                        Path("/test/path/method_name.ipynb"),
                        MethodKind.TrainingOptimization,
                    )

                    # Verify from_md_desc was called with correct parameters
                    mock_from_md_desc.assert_called_once()
                    args, kwargs = mock_from_md_desc.call_args
                    assert kwargs["slug"] == "method_name"
                    assert kwargs["kind"] == MethodKind.TrainingOptimization
                    assert "# Test Method" in kwargs["x"]
                    assert result == mock_method_info

    def test_from_file_without_markdown_cell_raises_exception(self):
        """Test that parsing fails for a notebook file without markdown cells."""
        # Create a mock notebook structure with only code cells
        nb = nbformat.v4.new_notebook()
        nb.cells = [
            nbformat.v4.new_code_cell("print('hello')"),
            nbformat.v4.new_code_cell("x = 1"),
        ]

        with patch("nbformat.read", return_value=nb):
            with patch("builtins.open", mock_open()):
                with pytest.raises(EmptyMethodDescription):
                    from_file(
                        Path("/test/path/method_name.ipynb"),
                        MethodKind.TrainingOptimization,
                    )

    def test_from_file_with_empty_markdown_cell_raises_exception(self):
        """Test that parsing fails for a notebook file with empty markdown cell."""
        # Create a mock notebook structure with an empty markdown cell
        nb = nbformat.v4.new_notebook()
        nb.cells = [
            nbformat.v4.new_code_cell("print('hello')"),
            nbformat.v4.new_markdown_cell(""),
        ]

        with patch("nbformat.read", return_value=nb):
            with patch("builtins.open", mock_open()):
                with pytest.raises(EmptyMethodDescription):
                    from_file(
                        Path("/test/path/method_name.ipynb"),
                        MethodKind.TrainingOptimization,
                    )

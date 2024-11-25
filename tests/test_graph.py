"""Tests for `sqlalchemy_db_graphing` package."""

from typing import Dict
import pydot
from tests.paths import TESTS_OUTPUT_PATH

from sqlalchemy_db_graphing import (
    generate_graph_as_pydot,
    generate_graph_as_png,
    generate_graph_as_svg,
)


def test_no_error_pydot(test_databases: Dict):
    """Test that the function returns a pydot.Dot object without raising an error."""
    for database in test_databases.values():
        graph = generate_graph_as_pydot(metadata=database.metadata)
        assert isinstance(graph, pydot.Dot)


def test_no_error_png(test_databases: Dict):
    """Test that the function writes a png."""
    for database_name, database in test_databases.items():
        file_name = TESTS_OUTPUT_PATH / f"{database_name}.png"
        generate_graph_as_png(metadata=database.metadata, filename=file_name)


def test_no_error_svg(test_databases: Dict):
    """Test that the function writes an svg."""
    for database_name, database in test_databases.items():
        file_name = TESTS_OUTPUT_PATH / f"{database_name}.svg"
        generate_graph_as_svg(metadata=database.metadata, filename=file_name)


def test_legend(test_databases: Dict):
    """Test that the legend is displayed when display_legend=True and not displayed when display_legend=False."""
    for database in test_databases.values():
        graph = generate_graph_as_pydot(metadata=database.metadata, display_legend=True)
        # Look for a node named "legend"
        assert "legend" in [node.get_name() for node in graph.get_nodes()]
        graph = generate_graph_as_pydot(
            metadata=database.metadata, display_legend=False
        )
        assert "legend" not in [node.get_name() for node in graph.get_nodes()]

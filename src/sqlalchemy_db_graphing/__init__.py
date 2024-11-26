"""Top-level package for Sqlalchemy DB graphing."""

from sqlalchemy_db_graphing.graph import (
    generate_graph_as_png,
    generate_graph_as_pydot,
    generate_graph_as_svg,
    get_schema_metadata_from_live_database,
)
from sqlalchemy_db_graphing.style_presets import DEFAULT_STYLE_OPTIONS, PRESETS

__author__ = """Erwan Nisol"""
__email__ = "erwan.nisol@free.fr"
__version__ = "0.2.0"
__all__ = [
    "generate_graph_as_png",
    "generate_graph_as_pydot",
    "generate_graph_as_svg",
    "get_schema_metadata_from_live_database",
    "DEFAULT_STYLE_OPTIONS",
    "PRESETS",
]

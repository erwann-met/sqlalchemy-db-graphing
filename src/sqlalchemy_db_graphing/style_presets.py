"""Module defining various style presets for graphs."""

from typing import Dict

import sqlalchemy_db_graphing.constants as cst


def generate_simple_preset(
    header_color: str, pk_color: str, fk_color: str = "white", rounded: bool = False
) -> Dict[str, str]:
    """Generate a simple preset for a graph with the given colors.

    Arguments
    ---------
    header_color : str
        The color of the header of the tables.
    pk_color : str
        The color of the primary keys of the tables.
    fk_color : str
        The color of the foreign keys of the tables. Default is white.
    rounded : bool
        Whether the tables should have rounded corners or not.
    """
    table_style = (
        "cellborder='1' cellspacing='0' cellpadding='4' border='1'"
        if not rounded
        else "cellborder='1' cellspacing='0' cellpadding='4' border='1' style='rounded'"
    )
    return {
        cst.TABLE_STYLE: table_style,
        cst.TABLE_NAME_STYLE: "color='white'",
        cst.HEADER_STYLE: f"align='center' bgcolor='{header_color}' border='0'",
        cst.SCHEMA_NAME_STYLE: "color='white'",
        cst.PK_STYLE: f"align='left' bgcolor='{pk_color}' border='0'",
        cst.FK_STYLE: f"align='left' bgcolor='{fk_color}' border='0'",
        cst.PK_FK_STYLE: f"align='left' bgcolor='{pk_color}' border='0'",
        cst.COLUMN_STYLE: "align='left' border='0'",
        cst.LEGEND_STYLE: "border='0' cellpadding='2' cellspacing='0'",
    }


MONOCHROMES_KWARGS = {
    "blue": {"header_color": "#3182BD", "pk_color": "#9ECAE1"},
    "green": {"header_color": "#31A354", "pk_color": "#C6EFC2"},
    "red": {"header_color": "#E6550D", "pk_color": "#FDAE6B"},
    "purple": {"header_color": "#756BB1", "pk_color": "#B2ABD2"},
    "orange": {"header_color": "#FF7F0E", "pk_color": "#FFC896"},
    "yellow": {"header_color": "#C9A700", "pk_color": "#FFF1AF"},
    "pink": {"header_color": "#FF7ABC", "pk_color": "#FFDBED"},
    "brown": {"header_color": "#8B4513", "pk_color": "#CCAB8C"},
    "gray": {"header_color": "#808080", "pk_color": "#D6D6D6"},
}

COLORS = {
    "red": "#FDAE6B",
    "blue": "#9ECAE1",
    "green": "#C6EFC2",
    "purple": "#B2ABD2",
    "orange": "#FFC896",
    "yellow": "#FFF1AF",
}


BICOLOR_KWARGS: Dict[str, Dict[str, str]] = {
    f"{color_1}_{color_2}": {"header_color": "#767676", "pk_color": COLORS[color_1], "fk_color": COLORS[color_2]}
    for color_1 in COLORS
    for color_2 in COLORS
    if color_1 != color_2
}

PRESETS = {
    name: generate_simple_preset(header_color=args["header_color"], pk_color=args["pk_color"])
    for name, args in MONOCHROMES_KWARGS.items()
}
PRESETS.update(
    {
        f"{name}_rounded": generate_simple_preset(
            header_color=args["header_color"], pk_color=args["pk_color"], rounded=True
        )
        for name, args in MONOCHROMES_KWARGS.items()
    }
)
PRESETS.update(
    {
        name: generate_simple_preset(header_color=args["header_color"], pk_color=args["pk_color"])
        for name, args in BICOLOR_KWARGS.items()
    }
)
PRESETS.update(
    {
        f"{name}_rounded": generate_simple_preset(
            header_color=args["header_color"], pk_color=args["pk_color"], rounded=True
        )
        for name, args in BICOLOR_KWARGS.items()
    }
)
PRESETS["default"] = cst.DEFAULT_STYLE_OPTIONS

DEFAULT_STYLE_OPTIONS = cst.DEFAULT_STYLE_OPTIONS

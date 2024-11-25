"""Script to generate a database schema diagram."""

from typing import Any, Dict, List

import pydot
from sqlalchemy import MetaData

import sqlalchemy_db_graphing.constants as cst


def read_model_metadata(metadata: MetaData) -> List[Dict[str, Any]]:
    """Read the metadata of a model and return a dictionary with the relevant information.

    Parameters
    ----------
    metadata : MetaData
        The metadata of the model to read. It can come from a declarative base or a running session.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionary with the metadata of each table.
    """
    simplified_metadata = []
    for table in metadata.sorted_tables:
        columns_data = []
        primary_keys = []
        foreign_keys_data = []
        foreign_keys = set()
        for fk in table.foreign_keys:
            foreign_keys_data.append(
                {
                    "target_table": fk.column.table.name,
                    "target_column": fk.column.name,
                    "column": fk.parent.name,
                }
            )
            foreign_keys.add(fk.parent.name)
        for pk in table.primary_key:
            primary_keys.append(pk.name)
        for column in table.columns:
            columns_data.append(
                {
                    "name": column.name,
                    "type": str(column.type),
                    "primary_key": column.name in primary_keys,
                    "foreign_key": column.name in foreign_keys,
                }
            )
        simplified_metadata.append(
            {
                "name": table.name,
                "schema": table.schema,
                "columns": columns_data,
                "foreign_keys": foreign_keys_data,
            }
        )
    return simplified_metadata


def generate_graph_as_pydot(
    metadata: MetaData,
    pk_color="#E4C087",
    fk_color="#F6EFBD",
    pk_and_fk_color="#BC7C7C",
    display_legend=True,
    **kwargs: Any,
) -> pydot.Dot:
    """Generate a database schema diagram as a pydot graph.

    Parameters
    ----------
    metadata : MetaData
        The metadata of the model to generate the diagram from.
    pk_color : str, optional
        Primary key color in the graph, by default "#E4C087"
    fk_color : str, optional
        Foreign key color in the graph, by default "#F6EFBD"
    pk_and_fk_color : str, optional
        Color of columns that are both a primary and a foreign key, by default "#BC7C7C"
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/

    Returns
    -------
    pydot.Dot
        A pydot graph with the database schema diagram.
    """
    info_dict = read_model_metadata(metadata)
    graph = pydot.Dot(**kwargs)
    # Add nodes
    for table in info_dict:
        graph.add_node(
            pydot.Node(
                name=table["name"],
                shape="plaintext",
                label=generate_table_html(
                    table_dict=table,
                    pk_color=pk_color,
                    fk_color=fk_color,
                    pk_and_fk_color=pk_and_fk_color,
                ),
            )
        )
    # Add edges
    for table in info_dict:
        for fk in table["foreign_keys"]:
            graph.add_edge(
                pydot.Edge(
                    src=fk["target_table"],
                    dst=table["name"],
                    headlabel=fk["column"],
                    taillabel=fk["target_column"],
                    minlen=2,
                )
            )
    # Add legend
    if display_legend:
        legend_html = "<<table border='0' cellpadding='2' cellspacing='0'>"
        legend_html += "<tr><td><b>Legend</b></td></tr>"
        legend_html += f"<tr><td align='left' bgcolor='{pk_color}'>Primary Key</td></tr>"
        legend_html += f"<tr><td align='left' bgcolor='{fk_color}'>Foreign Key</td></tr>"
        legend_html += f"<tr><td align='left' bgcolor='{pk_and_fk_color}'>Primary and Foreign Key</td></tr>"
        legend_html += "</table>>"
        graph.add_node(pydot.Node("legend", shape="rectangle", label=legend_html))
    return graph


def generate_table_html(table_dict, pk_color, fk_color, pk_and_fk_color):
    if (schema := table_dict["schema"]) is not None:
        table_name_html = cst.HTML_TABLE_NAME_WITH_SCHEMA.format(
            schema=schema, table_name=table_dict["name"], color="red"
        )
    else:
        table_name_html = cst.HTML_TABLE_NAME_WITHOUT_SCHEMA.format(table_name=table_dict["name"], color="red")
    table_html = cst.HTML_TABLE_HEADER.format(table_html=table_name_html)
    for column in table_dict["columns"]:
        displayed_name = f"{column['name']} ({column['type']})"
        if column["primary_key"] and column["foreign_key"]:
            color = pk_and_fk_color
        elif column["primary_key"]:
            color = pk_color
        elif column["foreign_key"]:
            color = fk_color
        else:
            color = "white"
        table_html += cst.HTML_COLUMN.format(color=color, displayed_name=displayed_name)
    table_html += "</table>>"
    return table_html


def generate_graph_as_png(
    metadata: MetaData,
    filename: str,
    pk_color="#E4C087",
    fk_color="#F6EFBD",
    pk_and_fk_color="#BC7C7C",
    display_legend=True,
    **kwargs: Any,
) -> None:
    """Generate a database schema diagram as a PNG file.

    Parameters
    ----------
    metadata : MetaData
        The metadata of the model to generate the diagram from.
    filename : str
        The name of the file to save the diagram to.
    pk_color : str, optional
        Primary key color in the graph, by default "#E4C087"
    fk_color : str, optional
        Foreign key color in the graph, by default "#F6EFBD"
    pk_and_fk_color : str, optional
        Color of columns that are both a primary and a foreign key, by default "#BC7C7C"
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/
    """
    graph = generate_graph_as_pydot(metadata, pk_color, fk_color, pk_and_fk_color, display_legend, **kwargs)
    graph.write_png(filename)


def generate_graph_as_svg(
    metadata: MetaData,
    filename: str,
    pk_color="#E4C087",
    fk_color="#F6EFBD",
    pk_and_fk_color="#BC7C7C",
    display_legend=True,
    **kwargs: Any,
) -> None:
    """Generate a database schema diagram as a SVG file.

    Parameters
    ----------
    metadata : MetaData
        The metadata of the model to generate the diagram from.
    filename : str
        The name of the file to save the diagram to.
    pk_color : str, optional
        Primary key color in the graph, by default "#E4C087"
    fk_color : str, optional
        Foreign key color in the graph, by default "#F6EFBD"
    pk_and_fk_color : str, optional
        Color of columns that are both a primary and a foreign key, by default "#BC7C7C"
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/
    """
    graph = generate_graph_as_pydot(metadata, pk_color, fk_color, pk_and_fk_color, display_legend, **kwargs)
    graph.write_svg(filename)

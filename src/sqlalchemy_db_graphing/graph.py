"""Script to generate a database schema diagram."""

from typing import Any, Dict, List, Optional, Union

import pydot
from sqlalchemy import MetaData, create_engine

import sqlalchemy_db_graphing.constants as cst
from sqlalchemy_db_graphing.style_presets import PRESETS


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
    style_options: Optional[Union[str, Dict[str, str]]] = None,
    display_legend=True,
    **kwargs: Any,
) -> pydot.Dot:
    """Generate a database schema diagram as a pydot graph.

    Parameters
    ----------
    metadata : MetaData
        The metadata of the model to generate the diagram from.
    style_options : Optional[Union[str, Dict[str, str]]]
        A string with the name of a preset style.
        Or a dictionary with the style options for the tables. See https://graphviz.org/doc/info/shapes.html#html for
        supported styles. Style strings are expected to be in the format "key1='value1' key2='value2'".
        Example: "align='center' bgcolor='grey' border='0'".
        Possible keys:
            - `table_style`: Style of each table (table element).
            - `table_name_style`: Style of the table name (font element).
            - `header_style`: Style of the table headers (td element).
            - `schema_name_style`: Style of the schema name (font element).
            - `pk_style`: Style of a column identified as a primary key (td element).
            - `fk_style`: Style of a column identified as a foreign key (td element).
            - `pk_fk_style`: Style of a column identified as both a primary and foreign key (td element).
            - `column_style`: Style of all other columns (td element).
            - `legend_style`: Style of the legend (table element).
        Missing keys will use the default style.
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/

    Returns
    -------
    pydot.Dot
        A pydot graph with the database schema diagram.

    Raises
    ------
    ValueError
        If the style options are not recognized.
    """
    if style_options is None:
        style_options = cst.DEFAULT_STYLE_OPTIONS
    elif isinstance(style_options, str):
        if style_options not in PRESETS:
            raise ValueError(
                f"Style options '{style_options}' not recognized. Available presets: {list(PRESETS.keys())}"
            )
        style_options = PRESETS[style_options]
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
                    style_options=style_options,
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
        legend_html = cst.HTML_LEGEND.format(legend_style=style_options.get(cst.LEGEND_STYLE, cst.DEFAULT_LEGEND_STYLE))
        legend_html += cst.HTML_COLUMN.format(
            column_style=style_options.get(cst.PK_STYLE, cst.DEFAULT_PK_STYLE),
            displayed_name="Primary Key",
        )
        legend_html += cst.HTML_COLUMN.format(
            column_style=style_options.get(cst.FK_STYLE, cst.DEFAULT_FK_STYLE),
            displayed_name="Foreign Key",
        )
        legend_html += cst.HTML_COLUMN.format(
            column_style=style_options.get(cst.PK_FK_STYLE, cst.DEFAULT_PK_FK_STYLE),
            displayed_name="Primary and Foreign Key",
        )
        legend_html += "</table>>"
        graph.add_node(pydot.Node("legend", shape="rectangle", label=legend_html))
    return graph


def generate_table_html(table_dict: Dict[str, Any], style_options: Dict[str, str]) -> str:
    """Generate the HTML code for a table in the graph.

    Parameters
    ----------
    table_dict : Dict[str, Any]
        A dictionary with the metadata of the table.
    style_options : Dict[str, str]
        A dictionary with the style options for the tables. See https://graphviz.org/doc/info/shapes.html#html for
        supported styles. Style strings are expected to be in the format "key1='value1' key2='value2'".
        Example: "align='center' bgcolor='grey' border='0'".
        Possible keys:
            - `table_style`: Style of each table (table element).
            - `table_name_style`: Style of the table name (font element).
            - `header_style`: Style of the table headers (td element).
            - `schema_name_style`: Style of the schema name (font element).
            - `pk_style`: Style of a column identified as a primary key (td element).
            - `fk_style`: Style of a column identified as a foreign key (td element).
            - `pk_fk_style`: Style of a column identified as both a primary and foreign key (td element).
            - `column_style`: Style of all other columns (td element).
            - `legend_style`: Style of the legend (table element).
        Missing keys will use the default style.

    Returns
    -------
    str
        The HTML code for the table.
    """
    if (schema := table_dict["schema"]) is not None:
        table_name_html = cst.HTML_TABLE_NAME_WITH_SCHEMA.format(
            schema=schema,
            table_name=table_dict["name"],
            schema_name_style=style_options.get(cst.SCHEMA_NAME_STYLE, cst.DEFAULT_SCHEMA_NAME_STYLE),
            table_name_style=style_options.get(cst.TABLE_NAME_STYLE, cst.DEFAULT_TABLE_NAME_STYLE),
        )
    else:
        table_name_html = cst.HTML_TABLE_NAME_WITHOUT_SCHEMA.format(
            table_name=table_dict["name"],
            table_name_style=style_options.get(cst.TABLE_NAME_STYLE, cst.DEFAULT_TABLE_NAME_STYLE),
        )
    table_html = cst.HTML_TABLE_HEADER.format(
        table_style=style_options.get(cst.TABLE_STYLE, cst.DEFAULT_TABLE_STYLE),
        header_style=style_options.get(cst.HEADER_STYLE, cst.DEFAULT_HEADER_STYLE),
        table_html=table_name_html,
    )
    for column in table_dict["columns"]:
        displayed_name = f"{column['name']} ({column['type']})"
        if column["primary_key"] and column["foreign_key"]:
            column_style = style_options.get(cst.PK_FK_STYLE, cst.DEFAULT_PK_FK_STYLE)
        elif column["primary_key"]:
            column_style = style_options.get(cst.PK_STYLE, cst.DEFAULT_PK_STYLE)
        elif column["foreign_key"]:
            column_style = style_options.get(cst.FK_STYLE, cst.DEFAULT_FK_STYLE)
        else:
            column_style = style_options.get(cst.COLUMN_STYLE, cst.DEFAULT_COLUMN_STYLE)
        table_html += cst.HTML_COLUMN.format(column_style=column_style, displayed_name=displayed_name)
    table_html += "</table>>"

    return table_html


def generate_graph_as_png(
    metadata: MetaData,
    filename: str,
    style_options: Optional[Dict[str, str]] = None,
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
    style_options : Optional[Dict[str, str]]
        A dictionary with the style options for the tables. See https://graphviz.org/doc/info/shapes.html#html for
        supported styles. Style strings are expected to be in the format "key1='value1' key2='value2'".
        Example: "align='center' bgcolor='grey' border='0'".
        Possible keys:
            - `table_style`: Style of each table (table element).
            - `table_name_style`: Style of the table name (font element).
            - `header_style`: Style of the table headers (td element).
            - `schema_name_style`: Style of the schema name (font element).
            - `pk_style`: Style of a column identified as a primary key (td element).
            - `fk_style`: Style of a column identified as a foreign key (td element).
            - `pk_fk_style`: Style of a column identified as both a primary and foreign key (td element).
            - `column_style`: Style of all other columns (td element).
            - `legend_style`: Style of the legend (table element).
        Missing keys will use the default style.
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/
    """
    graph = generate_graph_as_pydot(
        metadata=metadata, style_options=style_options, display_legend=display_legend, **kwargs
    )
    graph.write_png(filename)


def generate_graph_as_svg(
    metadata: MetaData,
    filename: str,
    style_options: Optional[Dict[str, str]] = None,
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
    style_options : Optional[Dict[str, str]]
        A dictionary with the style options for the tables. See https://graphviz.org/doc/info/shapes.html#html for
        supported styles. Style strings are expected to be in the format "key1='value1' key2='value2'".
        Example: "align='center' bgcolor='grey' border='0'".
        Possible keys:
            - `table_style`: Style of each table (table element).
            - `table_name_style`: Style of the table name (font element).
            - `header_style`: Style of the table headers (td element).
            - `schema_name_style`: Style of the schema name (font element).
            - `pk_style`: Style of a column identified as a primary key (td element).
            - `fk_style`: Style of a column identified as a foreign key (td element).
            - `pk_fk_style`: Style of a column identified as both a primary and foreign key (td element).
            - `column_style`: Style of all other columns (td element).
            - `legend_style`: Style of the legend (table element).
        Missing keys will use the default style.
    display_legend : bool, optional
        Whether to display a legend in the graph, by default True
    **kwargs : Any
        Additional arguments to pass to the pydot.Dot constructor
        List of possible arguments: https://graphviz.org/docs/graph/
    """
    graph = generate_graph_as_pydot(
        metadata=metadata, style_options=style_options, display_legend=display_legend, **kwargs
    )
    graph.write_svg(filename)


def get_schema_metadata_from_live_database(url: str, schema: Optional[str] = None) -> MetaData:
    """Get the metadata of a database from a connexion string.

    Parameters
    ----------
    url= : str
        The url to the database.
    schema : Optional[str]
        The schema to get the metadata from. Defaults to None.

    Returns
    -------
    MetaData
        The metadata of the database.

    Raises
    ------
    DatabaseConnexionError
        If there is an issue with the database connexion.
    """
    try:
        engine = create_engine(url=url)
        metadata = MetaData()
        metadata.reflect(bind=engine, schema=schema)
        return metadata
    except Exception as e:
        raise DatabaseConnexionError("Error while connecting to the database. Is it running?") from e


class DatabaseConnexionError(Exception):
    """Error raised when there is an issue with the database connexion."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

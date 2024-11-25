""" Script to generate a database schema diagram. """
from typing import Any, Union, Dict
import pydot
from sqlalchemy import MetaData, Table


def read_model_metadata(metadata: Union[MetaData, Table]) -> Dict[str, Any]:
    """ Read the metadata of a model and return a dictionary with the relevant information.

    Parameters
    ----------
    metadata : Union[MetaData, Table]
        The metadata of the model to read. It can come from a declarative base or a running session.

    Returns
    -------
    Dict[str, Any]
        A dictionary with the metadata of the model.
    """
    if isinstance(metadata, MetaData):
        return [read_model_metadata(table) for table in metadata.sorted_tables]
    if isinstance(metadata, Table):
        columns_data = []
        primary_keys = []
        foreign_keys_data = []
        foreign_keys = set()
        for fk in metadata.foreign_keys:
            foreign_keys_data.append(
                {
                    "target_table": fk.column.table.name,
                    "target_column": fk.column.name,
                    "column": fk.parent.name,
                }
            )
            foreign_keys.add(fk.parent.name)
        for pk in metadata.primary_key:
            primary_keys.append(pk.name)
        for column in metadata.columns:
            columns_data.append({
                "name": column.name,
                "type": str(column.type),
                "primary_key": column.name in primary_keys,
                "foreign_key": column.name in foreign_keys,
            })
        return {
            "name": metadata.name,
            "schema": metadata.schema,
            "columns": columns_data,
            "foreign_keys": foreign_keys_data,
        }

def generate_graph_as_pydot(
        metadata: MetaData,
        pk_color="#E4C087", 
        fk_color="#F6EFBD",
        pk_and_fk_color="#BC7C7C", 
        display_legend = True,
        **kwargs: Any,
    ) -> pydot.Dot:
    """ Generate a database schema diagram as a pydot graph.

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
                table["name"],
                shape="plaintext",
                label=generate_table_html(table_dict=table, pk_color=pk_color, fk_color=fk_color, pk_and_fk_color=pk_and_fk_color),
            )
        )
    # Add edges
    for table in info_dict:
        for fk in table["foreign_keys"]:
            graph.add_edge(
                pydot.Edge(
                    fk["target_table"],
                    table["name"],
                    headlabel=fk['column'],
                    taillabel=fk['target_column'],
                    minlen = 2
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
    table_html = f"<<table border='1' cellpadding='5' cellspacing='0'><tr><td bgcolor='#DDDDDD'><b>{table_dict['schema']}.<font color='red'>{table_dict['name']}</font></b></td></tr>"
    for column in table_dict["columns"]:
        displayed_name = f"{column['name']} ({column['type']})"
        if column["primary_key"] and column["foreign_key"]:
            # Fill background with striped background alternating primary and foreign keys colors
            table_html += f"<tr><td align='left' bgcolor='{pk_and_fk_color}'>{displayed_name}</td></tr>"
        elif column["foreign_key"]:
            table_html += f"<tr><td align='left' bgcolor='{fk_color}'>{displayed_name}</td></tr>"
        elif column["primary_key"]:
            table_html += f"<tr><td align='left' bgcolor='{pk_color}'>{displayed_name}</td></tr>"
        else:
            table_html += f"<tr><td align='left'>{displayed_name}</td></tr>"
    table_html += "</table>>"
    return table_html


def generate_graph_as_png(
        metadata: MetaData,
        filename: str,
        pk_color="#E4C087", 
        fk_color="#F6EFBD",
        pk_and_fk_color="#BC7C7C", 
        display_legend = True,
        **kwargs: Any,
    ) -> None:
    """ Generate a database schema diagram as a PNG file.

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
    """
    graph = generate_graph_as_pydot(metadata, pk_color, fk_color, pk_and_fk_color, display_legend, **kwargs)
    graph.write_png(filename)

def generate_graph_as_svg(
        metadata: MetaData,
        filename: str,
        pk_color="#E4C087", 
        fk_color="#F6EFBD",
        pk_and_fk_color="#BC7C7C", 
        display_legend = True,
        **kwargs: Any,
    ) -> None:
    """ Generate a database schema diagram as a SVG file.

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
    """
    graph = generate_graph_as_pydot(metadata, pk_color, fk_color, pk_and_fk_color, display_legend, **kwargs)
    graph.write_svg(filename)

# Sqlalchemy DB graphing tool

A module to display sqlalchemy database tables and keys as a graph.


license: MIT license

## Features

Generate graphs from your sqlalchemy declarative database in one simple function call.

How to use:
```python
from sqlalchemy_db_graphing import generate_graph_as_png
from mymodule.database_schema import MySQLAlchemySchema

filename = "path/to/save/file.png"
generate_graph_as_png(metadata=MySQLAlchemySchema.metadata, filename=filename)
```
![Database Graph](diagrams/demo_app_schema.png)

`generate_graph_as_png` also supports basic arguments:
- `pk_color`: color of primary keys.
- `fk_color`: color of foreign keys.
- `pk_and_fk_color`: color of columns that are both a primary and a foreign key.
- `display_legend`: whether the legend is displayed or not.

Finally, it supports all graphviz arguments, see https://graphviz.org/docs/graph/ for a comprehensive list.
```
generate_graph_as_png(
        metadata=MySQLAlchemySchema.metadata,
        filename=filename,
        display_legend=True,
        rankdir="LR",  # Draw the graph from Left to Right instead of Top Down.
        splines = "ortho",
)
```
![Database Graph](diagrams/demo_app_schema_kwargs.png)

The module also includes a few other functions:
- `generate_graph_as_svg` for svg pictures generation.
- `generate_graph_as_pydot` to get a pydot representation of your declarative base.
- `get_schema_metadata_from_live_database` to retrieve the metadata from a live database instead of the declarative database

Example with live database:
```python
from sqlalchemy_db_graphing import get_schema_metadata_from_live_database

database_url = f"postgresql+asyncpg://username:password@host:port/db_name"
metadata = get_schema_metadata_from_live_database(url=database_url, schema="my_app_schema")
```

## Credits

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

- Cookiecutter: https://github.com/audreyr/cookiecutter
- `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

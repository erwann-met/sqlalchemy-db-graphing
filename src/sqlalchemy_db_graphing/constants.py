"""Module that contains constants for the project."""

HTML_TABLE_HEADER = "<<table {table_style}><tr><td {header_style}>{table_html}</td></tr>"
HTML_TABLE_NAME_WITH_SCHEMA = (
    "<b><font {schema_name_style}>{schema}.</font><font {table_name_style}>{table_name}</font></b>"
)
HTML_TABLE_NAME_WITHOUT_SCHEMA = "<b><font {table_name_style}>{table_name}</font></b>"
HTML_COLUMN = "<tr><td {column_style}>{displayed_name}</td></tr>"
HTML_LEGEND = "<<table {legend_style}><tr><td><b>Legend</b></td></tr>"

DEFAULT_PK_COLOR = "#E7CB94"
DEFAULT_FK_COLOR = "#CEDB9C"
DEFAULT_PK_FK_COLOR = "#E7969C"

DEFAULT_TABLE_STYLE = "cellborder='1' cellspacing='0' cellpadding='4' border='1' style='rounded'"
DEFAULT_TABLE_NAME_STYLE = "color='red'"
DEFAULT_HEADER_STYLE = "align='center' bgcolor='#BFBFBF' border='0'"
DEFAULT_SCHEMA_NAME_STYLE = "color='black'"
DEFAULT_PK_STYLE = f"align='left' bgcolor='{DEFAULT_PK_COLOR}' border='0'"
DEFAULT_FK_STYLE = f"align='left' bgcolor='{DEFAULT_FK_COLOR}' border='0'"
DEFAULT_PK_FK_STYLE = f"align='left' bgcolor='{DEFAULT_PK_FK_COLOR}' border='0'"
DEFAULT_COLUMN_STYLE = "align='left' border='0'"
DEFAULT_LEGEND_STYLE = "border='0' cellpadding='2' cellspacing='0'"

TABLE_STYLE = "table_style"
TABLE_NAME_STYLE = "table_name_style"
HEADER_STYLE = "header_style"
SCHEMA_NAME_STYLE = "schema_name_style"
PK_STYLE = "pk_style"
FK_STYLE = "fk_style"
PK_FK_STYLE = "pk_fk_style"
COLUMN_STYLE = "column_style"
LEGEND_STYLE = "legend_style"

DEFAULT_STYLE_OPTIONS = {
    TABLE_STYLE: DEFAULT_TABLE_STYLE,
    TABLE_NAME_STYLE: DEFAULT_TABLE_NAME_STYLE,
    HEADER_STYLE: DEFAULT_HEADER_STYLE,
    SCHEMA_NAME_STYLE: DEFAULT_SCHEMA_NAME_STYLE,
    PK_STYLE: DEFAULT_PK_STYLE,
    FK_STYLE: DEFAULT_FK_STYLE,
    PK_FK_STYLE: DEFAULT_PK_FK_STYLE,
    COLUMN_STYLE: DEFAULT_COLUMN_STYLE,
    LEGEND_STYLE: DEFAULT_LEGEND_STYLE,
}

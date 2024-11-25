"""Module that contains constants for the project."""

HTML_TABLE_HEADER = (
    "<<table border='1' cellpadding='5' cellspacing='0'><tr><td bgcolor='#DDDDDD'>{table_html}</td></tr>"
)
HTML_TABLE_NAME_WITH_SCHEMA = "<b>{schema}.<font color='{color}'>{table_name}</font></b>"
HTML_TABLE_NAME_WITHOUT_SCHEMA = "<b><font color='{color}'>{table_name}</font></b>"
HTML_COLUMN = "<tr><td align='left' bgcolor='{color}'>{displayed_name}</td></tr>"

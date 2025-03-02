from enum import Enum
from qfluentwidgets import StyleSheetBase, qconfig, Theme, theme


class StyleSheet(StyleSheetBase, Enum):
    PARSE_INTERFACE = "parse_interface"
    CUSTOM_TABLE = "table_view"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"app/resources/qss/{theme.value.lower()}/{self.value}.qss"
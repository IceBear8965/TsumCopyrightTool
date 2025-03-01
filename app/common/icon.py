from qfluentwidgets import FluentIconBase, Theme, getIconColor

from enum import Enum

class CustomIcons(FluentIconBase, Enum):
    TABLE = "table-solid"
    XLSX = "xlsx-file"
    LIST = "list"

    def path(self, theme = Theme.AUTO):
        return f'app/resources/images/icons/{self.value}_{getIconColor(theme)}.svg'
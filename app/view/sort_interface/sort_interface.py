from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF

from app.view.sort_interface.UI_SortInterface import Ui_SortInterface


class SortInterface(Ui_SortInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("sortInterface")
        self.useFiltersToggle.setChecked(True)
        self.useFiltersToggle.setOnText("Applying filters")
        self.useFiltersToggle.setOffText("Adding dots")
        self.sortBtn.setIcon(FIF.EDIT)
        self.copySortedBtn.setIcon(FIF.COPY)
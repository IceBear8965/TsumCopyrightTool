"""
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
"""

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition

from app.common.addDots import addDots
from app.common.sortInput import sortInput
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
        self.clipboard = QApplication.clipboard()

        # connect signal to slot
        self.sortBtn.clicked.connect(self.sorting)
        self.copySortedBtn.clicked.connect(self.copyToClipboard)

    def sorting(self):
        useFilters = self.useFiltersToggle.isChecked()
        filters, order = getSettings()
        sortdata = self.sortTextInput.toPlainText().split("\n")

        if useFilters:
            if len(filters) > 1 and len(order) > 1 and len(sortdata) > 1:
                sortdata = sortInput(sortdata, filters, order)
                output = addDots(sortdata)
                self.sortedOutput.setPlainText(output)
                self.sortTextInput.clear()
            else:
                InfoBar.warning(
                    title="Error",
                    content="Enter valid data, filters and order",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    parent=self,
                )
        else:
            if len(sortdata) > 1:
                data = []
                for i in sortdata:
                    if i != "":
                        data.append(i.strip())

                if len(data) != 0:
                    output = addDots(data)
                    self.sortedOutput.setPlainText(output)
                    self.sortTextInput.clear()
            else:
                InfoBar.warning(
                    title="Error",
                    content="Enter valid data",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    parent=self,
                )

    def copyToClipboard(self):
        if len(self.sortedOutput.toPlainText()) > 1:
            self.clipboard.setText(self.sortedOutput.toPlainText())
            InfoBar.success(
                title="Clipboard",
                content="Copied to clipboard",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=1000,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self,
            )
        else:
            InfoBar.warning(
                title="Error",
                content="Output field is empty",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self,
            )

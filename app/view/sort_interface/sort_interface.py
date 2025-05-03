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
from app.common.presetModel import presetModel
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
        filters, order = presetModel.getSetting()
        input_data = self.sortTextInput.toPlainText().split("\n")

        data = []
        for item in input_data:
            if item != "":
                data.append(item)

        if useFilters:
            if len(data) > 1:
                data = sortInput(data, filters, order)
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
        else:
            if len(data) > 1:
                data = []
                for i in data:
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

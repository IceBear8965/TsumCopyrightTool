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

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition, getIconColor

from app.common.parsers.arenaParser import parseArena
from app.common.parsers.kidisParser import parseKidis
from app.common.parsers.saksParser import parseSaks
from app.common.parsers.sauconyParser import parseSaucony
from app.common.presetModel import presetModel
from app.common.icon import CustomIcons
from app.view.parse_interface.UI_ParseInterface import Ui_ParseInterface
from app.common.set_website_names import set_website_names


class ParseInterface(Ui_ParseInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("parseInterface")
        self.parseBtn.setIcon(FIF.CLOUD_DOWNLOAD)
        self.copyParsedBtn.setIcon(FIF.COPY)
        self.clipboard = QApplication.clipboard()

        # Иконки при выборе имени сайта
        set_website_names(self.websiteNameCombo)  # Добавляет элементы выбора в комбо бокс

        # connect signal to slot
        self.parseBtn.clicked.connect(self.onParseBtnClicked)
        self.copyParsedBtn.clicked.connect(self.copyToClipboard)

    def onParseBtnClicked(self):
        global output
        websiteName = self.websiteNameCombo.currentText()
        url = self.inputUrl.text()
        filters, order = presetModel.getSetting()

        if len(url) > 10:
            match websiteName:
                case "Saks85":
                    try:
                        output = parseSaks(url, filters, order)
                        self.parsedOutput.setPlainText(output)
                    except Exception:
                        InfoBar.error(
                            title="Error",
                            content="Something went wrong",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            duration=2000,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            parent=self,
                        )
                case "Saucony":
                    try:
                        output = parseSaucony(url)
                        self.parsedOutput.setPlainText(output)
                    except Exception:
                        InfoBar.error(
                            title="Error",
                            content="Something went wrong",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            duration=2000,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            parent=self,
                        )
                case "Arena":
                    try:
                        output = parseArena(url)
                        self.parsedOutput.setPlainText(output)
                    except Exception:
                        InfoBar.error(
                            title="Error",
                            content="Something went wrong",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            duration=2000,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            parent=self,
                        )
                case "Kidis":
                    try:
                        output = parseKidis(url, filters, order)
                        self.parsedOutput.setPlainText(output)
                    except Exception:
                        InfoBar.error(
                            title="Error",
                            content="Something went wrong",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            duration=2000,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            parent=self,
                        )
        else:
            InfoBar.warning(
                title="Error",
                content="URL filed is empty",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self,
            )
        self.inputUrl.clear()

    def copyToClipboard(self):
        if len(self.parsedOutput.toPlainText()) > 1:
            self.clipboard.setText(self.parsedOutput.toPlainText())
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
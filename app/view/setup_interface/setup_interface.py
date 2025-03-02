'''
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
'''

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition
from app.common.config import cfg

from app.view.setup_interface.UI_SetupInterface import Ui_SetUpInterface


class SetupInterface(Ui_SetUpInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("setupInterface")
        self.saveSettingsBtn.setIcon(FIF.SAVE)
        self.saveSettingsBtn.clicked.connect(self.saveSettings)
        if len(cfg.filters.value) != 0:
            self.filtersEdit.setPlainText("\n".join(cfg.filters.value))
        if len(cfg.order.value) != 0:
            self.orderEdit.setPlainText("\n".join(cfg.order.value))

    def saveSettings(self):
        try:
            cfg.set(cfg.filters, self.filtersEdit.toPlainText().split("\n"))
            cfg.set(cfg.order, self.orderEdit.toPlainText().split("\n"))

            # Success info bar
            InfoBar.success(
                title='Save',
                content="Settings were saved successfully",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        except:
            InfoBar.error(
                title='Save',
                content="Settings were not saved",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
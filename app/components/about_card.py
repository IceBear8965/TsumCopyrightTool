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

from typing import Union
from qfluentwidgets import SettingCard, FluentIconBase, ToolButton

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QToolButton


class AboutCard(SettingCard):
    """Setting card with a push button"""

    clicked = pyqtSignal()

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------
        text: str
            the text of push button

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.button = ToolButton(parent=self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def setBtnIcon(self, icon: Union[QIcon, FluentIconBase]):
        self.button.setIcon(icon)

# coding:utf-8
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

from qfluentwidgets import (
    ComboBoxSettingCard,
    SwitchSettingCard,
    OptionsSettingCard,
    ExpandLayout,
    Theme,
    setTheme,
    isDarkTheme,
    setFont,
    SettingCardGroup,
    TitleLabel,
    ScrollArea,
    PushSettingCard,
)
from qfluentwidgets import FluentIcon as FIF

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog

from app.common.setting import DOCUMENT_FOLDER
from app.common.signal_bus import signalBus
from app.common.config import cfg
from app.common.icon import CustomIcons
from app.view.parse_interface.parse_interface import ParseInterface


class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = TitleLabel(self.tr("Settings"), self)

        # Folders group
        self.foldersGroup = SettingCardGroup(self.tr("Folders"), self.scrollWidget)
        self.outputFolderCard = PushSettingCard(
            self.tr("Select folder"),
            FIF.FOLDER_ADD,
            self.tr("Output folder"),
            cfg.get(cfg.outputFolder),
            parent=self.foldersGroup,
        )

        # personalization
        self.personalGroup = SettingCardGroup(self.tr("Personalization"), self.scrollWidget)
        self.themeCard = ComboBoxSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr("Application theme"),
            self.tr("Change the appearance of your application"),
            texts=[self.tr("Light"), self.tr("Dark"), self.tr("Use system setting")],
            parent=self.personalGroup,
        )
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr("Mica effect"),
            self.tr("Apply semi transparent to windows and surfaces"),
            cfg.micaEnabled,
            self.personalGroup,
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 100, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # initialize style sheet
        setFont(self.settingLabel, 23, QFont.Weight.DemiBold)
        self.enableTransparentBackground()

        # initialize layout
        self.__initLayout()
        self._connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 50)

        # folders
        self.foldersGroup.addSettingCard(self.outputFolderCard)

        # personalization
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.micaCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.foldersGroup)
        self.expandLayout.addWidget(self.personalGroup)

    def __onOutputFolderCardClicked(self):
        """download folder card clicked slot"""
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Select folder"), str(DOCUMENT_FOLDER), QFileDialog.ShowDirsOnly
        )
        if not folder or cfg.get(cfg.outputFolder) == folder:
            return

        cfg.set(cfg.outputFolder, folder)
        self.outputFolderCard.setContent(folder)

    # def _onThemeChanged(self):
    #     print(1)
    #     self.websiteNameCombo.setIcon(QIcon(CustomIcons[ParseInterface.websiteNameCombo.text()].path()))

    def _connectSignalToSlot(self):
        # personalization
        cfg.themeChanged.connect(setTheme)
        self.themeCard.comboBox.currentIndexChanged.connect(signalBus.themeChanged)
        self.micaCard.checkedChanged.connect(signalBus.micaEnableChanged)

        # Output folder
        self.outputFolderCard.clicked.connect(self.__onOutputFolderCardClicked)

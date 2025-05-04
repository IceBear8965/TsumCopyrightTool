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

import os
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (
    NavigationAvatarWidget,
    NavigationItemPosition,
    MessageBox,
    FluentWindow,
    SplashScreen,
    SystemThemeListener,
    isDarkTheme,
    setTheme,
    Theme,
)
from qfluentwidgets import FluentIcon as FIF

from app.common.presetModel import presetModel
from app.common.saver import Saver
from app.common.signal_bus import signalBus
from app.common.config import cfg
from app.common.icon import CustomIcons
from app.common.setting import SETTING_FILE, VERSION
from app.common.style_sheet import StyleSheet
from app.view.parse_interface.parse_interface import ParseInterface
from app.view.sort_interface.sort_interface import SortInterface
from app.view.excel_interface.excel_interface import ExcelInterface
from app.view.getLinks_interface.getLinks_interface import GetLinksInterface
from app.view.setup_interface.setup_interface import SetupInterface
from app.view.setting_interface.setting_interface import SettingInterface

basedir = os.path.dirname(__file__)

# Меняем дефолтный идентификатор приложухи на свой, чтоб винда правильно отображала иконку на панели задач
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = f'com.tsumcopyrighttool.{VERSION}'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.themeListener = SystemThemeListener(self)

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # Загружаем сохраненные пресеты
        self.presetsTemplate = {
            "current": "",
            "presets": {},
        }

        self.saver = Saver()
        if self.saver.load(SETTING_FILE):  # Проверка существует ли файл настроек
            self.savedData = self.saver.load(SETTING_FILE)
            presets = self.savedData.get("presets")

            if len(presets.keys()) > 0:  # Проверяем пустой или нет объект с прессетами
                keys = list(presets.keys())

                flag = False
                for key in keys:
                    preset = presets[key]
                    if isinstance(preset.get("filters"), str):
                        flag = True  # Переменная для проверки правильности фильтров

                if flag:
                    presetModel.presetsData = self.presetsTemplate
                    self.saver.save(SETTING_FILE, presetModel.presetsData)
                else:  # Если в первом пресете лежат строки, то пишем шаблон в модель и сохраняем шаблон в файл настроек
                    presetModel.presetsData = self.savedData

            else:  # Если объект с пресетами пустой, то пишем шаблон в модель и сохраняем шаблон в файл настроек
                presetModel.presetsData = self.presetsTemplate
                self.saver.save(SETTING_FILE, presetModel.presetsData)
        else:  # Если файла настроек нет, то грузим в модель шаблон и сохраняем файл настроек
            presetModel.presetsData = self.presetsTemplate
            self.saver.save(SETTING_FILE, presetModel.presetsData)

        self.parseInterface = ParseInterface(self)
        self.sortInterface = SortInterface(self)
        self.excelInterface = ExcelInterface(self)
        self.getLinksInterface = GetLinksInterface(self)
        self.setupInterface = SetupInterface(self)
        self.settingInterface = SettingInterface(self)

        self.connectSignalToSlot()

        self.initNavigation()
        self.themeListener.start()

    def initWindow(self):
        self.resize(860, 680)
        self.setMinimumWidth(760)
        self.setWindowTitle("Tsum Copyright Tool")
        self.setWindowIcon(QIcon(os.path.join(basedir, "../resources/images/tsumlogo.ico")))
        self.setObjectName("mainWindow")

        # loading data from file
        # self.saver = Saver()
        # self.savedData = self.saver.load(SETTING_FILE)
        # if self.saver.load(SETTING_FILE):
        #     presetModel.dataList = self.savedData

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.navigationInterface.setExpandWidth(180)
        self.addSubInterface(self.parseInterface, FIF.CLOUD_DOWNLOAD, self.tr("Parse"), NavigationItemPosition.SCROLL)
        self.addSubInterface(self.sortInterface, FIF.EDIT, self.tr("Sort"), NavigationItemPosition.SCROLL)
        self.addSubInterface(self.excelInterface, CustomIcons.XLSX, self.tr("Excel"), NavigationItemPosition.SCROLL)
        self.addSubInterface(self.getLinksInterface, CustomIcons.LINK, self.tr("Get Links"), NavigationItemPosition.SCROLL)
        self.addSubInterface(self.setupInterface, CustomIcons.LIST, self.tr("Presets"), NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr("Settings"), NavigationItemPosition.BOTTOM)

    def closeEvent(self, e):
        # Stop the listener thread
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # Retry mechanism needed when mica effect is enabled
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

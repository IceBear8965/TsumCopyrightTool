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

import sys

from qfluentwidgets import (QConfig, qconfig, Theme, ConfigItem, ConfigValidator, FolderValidator, BoolValidator, OptionsValidator)
from app.common.setting import CONFIG_FILE, DOCUMENT_FOLDER

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

class Config(QConfig):
    # folders
    outputFolder = ConfigItem("Folders", "OutputFolder", str(DOCUMENT_FOLDER), FolderValidator())

    # Personalization
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(str(CONFIG_FILE.absolute()), cfg)
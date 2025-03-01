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

    # Set up
    filters = ConfigItem("SetUp", "Filters", [], ConfigValidator())
    order = ConfigItem("SetUp", "Order", [], ConfigValidator())

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(str(CONFIG_FILE.absolute()), cfg)
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition
from app.view.parse_interface.UI_ParseInterface import Ui_ParseInterface

# from app.common.getSettings import getSettings
# from app.common.parsers.saksParser import parseSaks
# from app.common.parsers.sauconyParser import parseSaucony
# from app.common.parsers.arenaParser import parseArena

class ParseInterface(Ui_ParseInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("parseInterface")
        self.parseBtn.setIcon(FIF.CLOUD_DOWNLOAD)
        self.copyParsedBtn.setIcon(FIF.COPY)
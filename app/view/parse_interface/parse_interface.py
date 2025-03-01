from traceback import print_tb

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition
from app.view.parse_interface.UI_ParseInterface import Ui_ParseInterface
from app.common.signal_bus import signalBus

from app.common.getSettings import getSettings
from app.common.parsers.saksParser import parseSaks
from app.common.parsers.sauconyParser import parseSaucony
from app.common.parsers.arenaParser import parseArena

class ParseInterface(Ui_ParseInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("parseInterface")
        self.parseBtn.setIcon(FIF.CLOUD_DOWNLOAD)
        self.copyParsedBtn.setIcon(FIF.COPY)
        self.clipboard = QApplication.clipboard()

        # connect signal to slot
        self.parseBtn.clicked.connect(self.onParseBtnClicked)
        self.copyParsedBtn.clicked.connect(self.copyToClipboard)

    def onParseBtnClicked(self):
        global output
        websiteName = self.webSiteNameCombo.currentText()
        url = self.inputUrl.text()
        filters, order = getSettings()


        if len(url) > 10:
            match websiteName:
                case "Saks85":
                    try:
                        print(1)
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
                            parent=self
                        )
            match websiteName:
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
                            parent=self
                        )
            match websiteName:
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
                            parent=self
                        )
        self.inputUrl.clear()

    def copyToClipboard(self):
        self.clipboard.setText(self.parsedOutput.toPlainText())
        InfoBar.success(
            title="Clipboard",
            content="Copied to clipboard",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=1000,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self
        )
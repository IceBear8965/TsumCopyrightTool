from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from app.common.icon import CustomIcons
from app.common.setting import DOCUMENT_FOLDER

from app.components.file_card import FileCard
from app.view.excel_interface.UI_ExcelInterface import Ui_ExcelInterface


class ExcelInterface(Ui_ExcelInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("excelInterface")

        fileCard = FileCard(CustomIcons.XLSX,"Input Excel file", "", self)
        self.inputFileCard.addWidget(fileCard)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition
import openpyxl
from app.common.icon import CustomIcons

from app.common.setting import DOWNLOAD_FOLDER

from app.components.file_card import FileCard
from app.view.excel_interface.UI_ExcelInterface import Ui_ExcelInterface


class ExcelInterface(Ui_ExcelInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("excelInterface")
        self.toggleUrlParsing()
        self.useUrlToggle.setOnText("Parsing from url`s")
        self.useUrlToggle.setOffText("Formatting descriptions")
        self.progressBar.setProperty("value", 0)

        self.fileCard = FileCard(CustomIcons.XLSX,"Input Excel file", "", self)
        self.inputFileCard.addWidget(self.fileCard)

        # connect signal to slots
        self.fileCard.openButton.clicked.connect(self.getExcelFile)
        self.useUrlToggle.checkedChanged.connect(self.toggleUrlParsing)

    def toggleUrlParsing(self):
        if self.useUrlToggle.isChecked():
            self.websiteNameCombo.setEnabled(True)
        else:
            self.websiteNameCombo.setEnabled(False)

    def getExcelFile(self):
        excel_file, _ = QFileDialog.getOpenFileName(self, "Open file", str(DOWNLOAD_FOLDER), "Excel files (*.xlsx)")
        if excel_file != "":
            self.fileCard.setContent(excel_file)
            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active
            self.tablePreview.setRowCount(worksheet.max_row)
            self.tablePreview.setColumnCount(worksheet.max_column)
            for i in range(worksheet.max_column):
                self.tablePreview.setColumnWidth(i, 170)
            self.tablePreview.horizontalHeader().setVisible(False)

            listValues = list(worksheet.values)

            rowIndex = 0
            for row in listValues:
                colIndex = 0
                for column in row:
                    self.tablePreview.setItem(rowIndex, colIndex, QTableWidgetItem(column))
                    colIndex += 1
                rowIndex += 1
        else:
            InfoBar.warning(
                title="Error",
                content="Choose Excel file",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self
            )
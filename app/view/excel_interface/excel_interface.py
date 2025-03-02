from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QThread, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition, TableView
import openpyxl
from pathlib import Path

from app.common.icon import CustomIcons
from app.common.setting import DOWNLOAD_FOLDER, DOCUMENT_FOLDER
from app.common.config import cfg
from app.common.getSettings import getSettings
from app.common.formatExcel import formatExcel
from app.common.parseExcel import parseExcel
from app.common.writeToExcel import writeOutputToExcel

from app.components.file_card import FileCard
from app.view.excel_interface.UI_ExcelInterface import Ui_ExcelInterface


# Worker class for working with Excel
class ExcelParser(QObject):
    format_result = pyqtSignal(list)
    parse_result = pyqtSignal(list)

    @pyqtSlot(str, int, str, list, list)
    def parseExcelInThread(self, excel_file, columnIndex, websiteName, filters, order):
        data = parseExcel(excel_file, columnIndex, websiteName, filters, order)
        self.parse_result.emit(data)

    @pyqtSlot(str, int, list, list)
    def formatExcelInThread(self, excel_file, columnIndex, filters, order):
        data = formatExcel(excel_file, columnIndex, filters, order)
        self.format_result.emit(data)

class ExcelInterface(Ui_ExcelInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("excelInterface")
        self.toggleUrlParsing()
        self.useUrlToggle.setOnText("Parsing from url`s")
        self.useUrlToggle.setOffText("Formatting descriptions")
        self.progressBar.setProperty("value", 0)

        # Multithreading
        self.ExcelParser = ExcelParser()
        self.ExcelThread = QThread()
        self.ExcelParser.parse_result.connect(self.on_parse_excel_result_ready)
        self.ExcelParser.format_result.connect(self.on_format_excel_result_ready)
        self.ExcelParser.moveToThread(self.ExcelThread)
        self.ExcelThread.start()

        self.fileCard = FileCard(CustomIcons.XLSX,"Input Excel file", "", self)
        self.inputFileCard.addWidget(self.fileCard)

        # connect signal to slots
        self.useUrlToggle.checkedChanged.connect(self.toggleUrlParsing)
        self.fileCard.openButton.clicked.connect(self.getExcelFile)
        self.excelRunBtn.clicked.connect(self.parseExcel)

    def toggleUrlParsing(self):
        if self.useUrlToggle.isChecked():
            self.websiteNameCombo.setEnabled(True)
        else:
            self.websiteNameCombo.setEnabled(False)

    # Multithreading get results from ExcelParser worker
    def on_format_excel_result_ready(self, output):
        writeOutputToExcel(output, cfg.get(cfg.outputFolder))
        print("Formatted")

    def on_parse_excel_result_ready(self, output):
        writeOutputToExcel(output, cfg.get(cfg.outputFolder))
        print("Parsed")

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
            self.tablePreview.horizontalHeader().hide()

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

    # Write data to Excel file
    def parseExcel(self):
        excel_file = self.fileCard.contentLabel.text()
        column = self.tablePreview.selectedItems()
        websiteName = self.websiteNameCombo.currentText()
        columnIndex = None
        file_extension = Path(excel_file).suffix
        if len(column) > 0:
            columnIndex = column[0].column()
        filters, paramorder = getSettings()

        if isinstance(columnIndex, int) and excel_file != "File path" and len(
                excel_file) > 10 and file_extension == ".xlsx":

            if self.useUrlToggle.isChecked():
                # Отправка в поток параметры подключения
                QMetaObject.invokeMethod(self.ExcelParser, 'parseExcelInThread',
                                                Qt.ConnectionType.QueuedConnection,
                                                Q_ARG(str, excel_file),
                                                Q_ARG(int, columnIndex),
                                                Q_ARG(str, websiteName),
                                                Q_ARG(list, filters),
                                                Q_ARG(list, paramorder))
            else:
                QMetaObject.invokeMethod(self.ExcelParser, 'formatExcelInThread',
                                                Qt.ConnectionType.QueuedConnection,
                                                Q_ARG(str, excel_file),
                                                Q_ARG(int, columnIndex),
                                                Q_ARG(list, filters),
                                                Q_ARG(list, paramorder))
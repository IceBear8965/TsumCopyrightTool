import time

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QThread, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition, TableView
import openpyxl
from pathlib import Path

from app.common.addDots import addDots
from app.common.icon import CustomIcons
from app.common.setting import DOWNLOAD_FOLDER, DOCUMENT_FOLDER
from app.common.config import cfg
from app.common.getSettings import getSettings
from app.common.parsers.saksParser import parseSaks
from app.common.parsers.sauconyParser import parseSaucony
from app.common.parsers.arenaParser import parseArena
from app.common.sortInput import sortInput
from app.common.writeToExcel import writeOutputToExcel

from app.components.file_card import FileCard
from app.view.excel_interface.UI_ExcelInterface import Ui_ExcelInterface


# Worker class for working with Excel
class ExcelParser(QObject):
    format_result = pyqtSignal(list)
    parse_result = pyqtSignal(list)
    progress_signal = pyqtSignal(int)

    @pyqtSlot(str, int, str, list, list)
    def parseExcelInThread(self, excel_file, columnIndex, websiteName, filters, order):
        global parsedData
        dataWorkbook = openpyxl.load_workbook(excel_file)
        dataWorksheet = dataWorkbook.active

        sources = []
        for c in list(dataWorksheet.values):
            sources.append(c[columnIndex])

        data = []
        i = 1
        for source in sources:
            try:
                match (websiteName):
                    case "Saks85":
                        parsedData = parseSaks(source, filters, order)
                    case "Saucony":
                        parsedData = parseSaucony(source)
                    case "Arena":
                        parsedData = parseArena(source)
            except Exception:
                parsedData = None
            self.progress_signal.emit(i)
            i += 1
            data.append(parsedData)

        self.parse_result.emit(data)

    @pyqtSlot(str, int, list, list)
    def formatExcelInThread(self, excel_file, columnIndex, filters, order):
        dataWorkbook = openpyxl.load_workbook(excel_file)
        dataWorksheet = dataWorkbook.active

        data = []
        for c in list(dataWorksheet.values):
            data.append(c[columnIndex])
        sortData = []
        for d in data:
            if d is not None:
                sortData.append(d)
        firstItem = sortData.pop(0)

        output = []
        i = 1
        for d in sortData:
            sorted = sortInput(d.split("\n"), filters, order)
            dotted = addDots(sorted)
            output.append(dotted)
            self.progress_signal.emit(i)
            i += 1
        output.insert(0, firstItem)

        self.format_result.emit(output)


class ExcelInterface(Ui_ExcelInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.max_row = None
        self.max_column = None
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
        self.ExcelParser.progress_signal.connect(self.progressUpdate)
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
        InfoBar.success(
            title="Formatting",
            content="Excel table formatted successfully",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self
        )

    def on_parse_excel_result_ready(self, output):
        writeOutputToExcel(output, cfg.get(cfg.outputFolder))
        InfoBar.success(
            title="Parsing",
            content="Excel table parsed successfully",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self
        )

    def progressUpdate(self, value):
        self.progressBar.setValue(value)

    def getExcelFile(self):
        excel_file, _ = QFileDialog.getOpenFileName(self, "Open file", str(DOWNLOAD_FOLDER), "Excel files (*.xlsx)")
        if excel_file != "":
            self.fileCard.setContent(excel_file)
            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active
            self.max_row = worksheet.max_row
            self.max_column = worksheet.max_column
            self.tablePreview.setRowCount(self.max_row)
            self.tablePreview.setColumnCount(self.max_column)
            for i in range(self.max_column):
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
                self.progressBar.setValue(0)
                self.progressBar.setRange(0, self.max_row-1)
                InfoBar.success(
                    title="Parsing",
                    content="Parsing your table",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self
                )
            else:
                QMetaObject.invokeMethod(self.ExcelParser, 'formatExcelInThread',
                                                Qt.ConnectionType.QueuedConnection,
                                                Q_ARG(str, excel_file),
                                                Q_ARG(int, columnIndex),
                                                Q_ARG(list, filters),
                                                Q_ARG(list, paramorder))
                self.progressBar.setValue(0)
                self.progressBar.setRange(0, self.max_row-1)
                InfoBar.success(
                    title="Formatting",
                    content="Formatting your table",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self
                )
        else:
            InfoBar.warning(
                title="Error",
                content="Select file and select column in preview",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self
            )
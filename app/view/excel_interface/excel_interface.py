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

from pathlib import Path

import openpyxl
from PyQt5.QtCore import Q_ARG, QMetaObject, QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QWidget
from qfluentwidgets import InfoBar, InfoBarPosition, RadioButton

from app.common.addDots import addDots
from app.common.presetModel import presetModel
from app.common.config import cfg
from app.common.excelHandler import excelHandler
from app.common.icon import CustomIcons
from app.common.parsers.arenaParser import parseArena
from app.common.parsers.kidisParser import parseKidis
from app.common.parsers.saksParser import parseSaks
from app.common.parsers.sauconyParser import parseSaucony
from app.common.saver import Saver
from app.common.setting import DOWNLOAD_FOLDER
from app.common.sortInput import sortInput
from app.components.file_card import FileCard
from app.view.excel_interface.UI_ExcelInterface import Ui_ExcelInterface


# Worker class for working with Excel
class ExcelParser(QObject):
    format_result = pyqtSignal(list)
    parse_result = pyqtSignal(list)
    progress_signal = pyqtSignal(int)

    @pyqtSlot(str, str, int, str, list, list)
    def parseExcelInThread(self, excel_file, excel_sheet, columnIndex, websiteName, filters, order):
        global parsedData
        dataWorkbook = openpyxl.load_workbook(excel_file)
        dataWorksheet = dataWorkbook[excel_sheet]

        sources = []
        for c in list(dataWorksheet.values):
            sources.append(c[columnIndex])

        data = []
        i = 1
        for source in sources:
            try:
                match websiteName:
                    case "Saks85":
                        parsedData = parseSaks(source, filters, order)
                    case "Saucony":
                        parsedData = parseSaucony(source)
                    case "Arena":
                        parsedData = parseArena(source)
                    case "Kidis":
                        parsedData = parseKidis(source, filters, order)
            except Exception:
                parsedData = None
            self.progress_signal.emit(i)
            i += 1
            data.append(parsedData)

        self.parse_result.emit(data)
        dataWorkbook.close()

    @pyqtSlot(str, str, int, list, list)
    def formatExcelInThread(self, excel_file, excel_sheet, columnIndex, filters, order):
        dataWorkbook = openpyxl.load_workbook(excel_file)
        dataWorksheet = dataWorkbook[excel_sheet]

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
        dataWorkbook.close()


class ExcelInterface(Ui_ExcelInterface, QWidget):
    sheetChanged = pyqtSignal(list, int, int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.current_workbook = None
        self.current_sheet = ""
        self.current_values = []
        self.setObjectName("excelInterface")
        self.toggleUrlParsing()
        self.tablePreview.verticalHeader().show()
        self.useUrlToggle.setOnText("Parsing from url`s")
        self.useUrlToggle.setOffText("Formatting descriptions")
        self.progressBar.setProperty("value", 0)
        self.sheetsView.enableTransparentBackground()
        self.saver = Saver()

        # Multithreading
        self.ExcelParser = ExcelParser()
        self.ExcelThread = QThread()
        self.ExcelParser.parse_result.connect(self.on_parse_excel_result_ready)
        self.ExcelParser.format_result.connect(self.on_format_excel_result_ready)
        self.ExcelParser.progress_signal.connect(self.progressUpdate)
        self.ExcelParser.moveToThread(self.ExcelThread)
        self.ExcelThread.start()

        self.fileCard = FileCard(CustomIcons.XLSX, "Input Excel file", "", self)
        self.inputFileCard.addWidget(self.fileCard)

        # connect signal to slots
        self.useUrlToggle.checkedChanged.connect(self.toggleUrlParsing)
        self.fileCard.openButton.clicked.connect(self.getExcelFile)
        self.excelRunBtn.clicked.connect(self.processExcel)
        self.sheetChanged.connect(self.loadExcelTable)

    # Интерфейс
    def toggleUrlParsing(self):
        if self.useUrlToggle.isChecked():
            self.websiteNameCombo.setEnabled(True)
        else:
            self.websiteNameCombo.setEnabled(False)

    def getExcelFile(self):
        excel_file, _ = QFileDialog.getOpenFileName(self, "Open file", str(DOWNLOAD_FOLDER), "Excel files (*.xlsx)")
        if excel_file != "":
            self.onNewFileLoaded()
            self.fileCard.setContent(excel_file)
            self.tablePreview.clearSelection()
            wb = openpyxl.load_workbook(excel_file, read_only=True)
            self.current_workbook = wb
            ws = wb.active
            values, max_row, max_column = excelHandler.getData(ws)
            self.loadExcelTable(values, max_row, max_column)
            self.setSheets(wb)
            self.current_values = values
        else:
            InfoBar.warning(
                title="Error",
                content="Choose Excel file",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self,
            )

    def setSheets(self, workbook):
        sheetNames = workbook.sheetnames
        for sheet in sheetNames:
            btn = RadioButton(sheet)
            btn.sheet = sheet
            btn.clicked.connect(self.sheetToggled)
            self.horizontalLayout_3.addWidget(btn, 0, Qt.AlignTop)
        first_btn = self.horizontalLayout_3.itemAt(0).widget()
        first_btn.setChecked(True)

        # horizontalLayout_3 -- лейаут в scrollArea, хрен знает как переименовать его из дизайнера

    def loadExcelTable(self, values, max_row, max_column):
        self.current_values = values
        self.tablePreview.setRowCount(max_row)
        self.tablePreview.setColumnCount(max_column)
        for i in range(max_column):
            self.tablePreview.setColumnWidth(i, 170)
        self.tablePreview.horizontalHeader().hide()

        rowIndex = 0
        for row in values:
            colIndex = 0
            for column in row:
                try:
                    self.tablePreview.setItem(rowIndex, colIndex, QTableWidgetItem(column))
                except Exception:
                    self.tablePreview.setItem(rowIndex, colIndex, QTableWidgetItem(None))
                colIndex += 1
            rowIndex += 1

    def sheetToggled(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            self.current_sheet = self.current_workbook[radiobutton.sheet]
            values, max_row, max_column = excelHandler.getData(self.current_sheet)
            self.sheetChanged.emit(values, max_row, max_column)

    # removing sheets in scroll area when new file is uploaded
    def onNewFileLoaded(self):
        for i in reversed(range(self.horizontalLayout_3.count())):
            self.horizontalLayout_3.itemAt(i).widget().setParent(None)

    # Write data to Excel file
    def processExcel(self):
        excel_file = self.fileCard.contentLabel.text()
        column = self.tablePreview.selectedItems()
        websiteName = self.websiteNameCombo.currentText()
        columnIndex = None
        file_extension = Path(excel_file).suffix
        if len(column) > 0:
            columnIndex = column[0].column()
        filters, paramorder = presetModel.getSetting()

        if isinstance(columnIndex, int) and excel_file != "" and len(excel_file) > 10 and file_extension == ".xlsx":
            if self.useUrlToggle.isChecked():  # парсинг
                # Отправка в поток-обработчик
                QMetaObject.invokeMethod(
                    self.ExcelParser,
                    "parseExcelInThread",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, excel_file),
                    Q_ARG(str, self.current_sheet),
                    Q_ARG(int, columnIndex),
                    Q_ARG(str, websiteName),
                    Q_ARG(list, filters),
                    Q_ARG(list, paramorder),
                )
                self.progressBar.setValue(0)
                self.progressBar.setRange(0, self.max_row - 1)
                self.fileCard.openButton.setEnabled(False)
                self.excelRunBtn.setEnabled(False)
                InfoBar.success(
                    title="Parsing",
                    content="Parsing your table",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self,
                )
            else:  # форматирование
                QMetaObject.invokeMethod(
                    self.ExcelParser,
                    "formatExcelInThread",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, excel_file),
                    Q_ARG(str, self.current_sheet),
                    Q_ARG(int, columnIndex),
                    Q_ARG(list, filters),
                    Q_ARG(list, paramorder),
                )
                self.progressBar.setValue(0)
                self.progressBar.setRange(0, self.max_row - 1)
                self.fileCard.openButton.setEnabled(False)
                self.excelRunBtn.setEnabled(False)
                InfoBar.success(
                    title="Formatting",
                    content="Formatting your table",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title="Error",
                content="Select file and select column in preview",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )

    # Multithreading get results from ExcelParser worker
    def on_format_excel_result_ready(self, output):
        self.saver.saveToExcel(output, cfg.get(cfg.outputFolder))
        self.fileCard.openButton.setEnabled(True)
        self.excelRunBtn.setEnabled(True)
        InfoBar.success(
            title="Formatting",
            content="Excel table formatted successfully",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

    def on_parse_excel_result_ready(self, output):
        self.saver.saveToExcel(output, cfg.get(cfg.outputFolder))
        self.fileCard.openButton.setEnabled(True)
        self.excelRunBtn.setEnabled(True)
        InfoBar.success(
            title="Parsing",
            content="Excel table parsed successfully",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

    def progressUpdate(self, value):
        self.progressBar.setValue(value)

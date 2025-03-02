from typing import List, Union

from PyQt5.QtCore import QModelIndex, Qt, QItemSelectionModel, pyqtProperty
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QAbstractItemView, QTableView

from qfluentwidgets import TableItemDelegate, setCustomStyleSheet, SmoothScrollDelegate

from app.common.style_sheet import StyleSheet

class TableBase:
    """ Table base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = TableItemDelegate(self)
        self.scrollDelagate = SmoothScrollDelegate(self)
        self._isSelectRightClickedRow = False

        # set style sheet
        # FluentStyleSheet.TABLE_VIEW.apply(self)
        StyleSheet.CUSTOM_TABLE.apply(self)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setAlternatingRowColors(True)
        self.setItemDelegate(self.delegate)
        self.setSelectionBehavior(CustomTable.SelectRows)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setDefaultSectionSize(38)

        self.entered.connect(lambda i: self._setHoverRow(i.row()))
        self.pressed.connect(lambda i: self._setPressedRow(i.row()))
        self.verticalHeader().sectionClicked.connect(self.selectRow)

    def setBorderVisible(self, isVisible: bool):
        """ set the visibility of border """
        self.setProperty("isBorderVisible", isVisible)
        self.setStyle(QApplication.style())

    def setBorderRadius(self, radius: int):
        """ set the radius of border """
        qss = f"QTableView{{border-radius: {radius}px}}"
        setCustomStyleSheet(self, qss, qss)

    def _setHoverRow(self, row: int):
        """ set hovered row """
        self.delegate.setHoverRow(row)
        self.viewport().update()

    def _setPressedRow(self, row: int):
        """ set pressed row """
        if self.selectionMode() == QTableView.SelectionMode.NoSelection:
            return

        self.delegate.setPressedRow(row)
        self.viewport().update()

    def _setSelectedRows(self, indexes: List[QModelIndex]):
        if self.selectionMode() == QTableView.SelectionMode.NoSelection:
            return

        self.delegate.setSelectedRows(indexes)
        self.viewport().update()

    def leaveEvent(self, e):
        QTableView.leaveEvent(self, e)
        self._setHoverRow(-1)

    def resizeEvent(self, e):
        QTableView.resizeEvent(self, e)
        self.viewport().update()

    def keyPressEvent(self, e: QKeyEvent):
        QTableView.keyPressEvent(self, e)
        self.updateSelectedRows()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton or self._isSelectRightClickedRow:
            return QTableView.mousePressEvent(self, e)

        index = self.indexAt(e.pos())
        if index.isValid():
            self._setPressedRow(index.row())

        QWidget.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        QTableView.mouseReleaseEvent(self, e)
        self.updateSelectedRows()

        if self.indexAt(e.pos()).row() < 0 or e.button() == Qt.RightButton:
            self._setPressedRow(-1)

    def setItemDelegate(self, delegate: TableItemDelegate):
        self.delegate = delegate
        super().setItemDelegate(delegate)

    def selectAll(self):
        QTableView.selectAll(self)
        self.updateSelectedRows()

    def selectRow(self, row: int):
        QTableView.selectRow(self, row)
        self.updateSelectedRows()

    def clearSelection(self):
        QTableView.clearSelection(self)
        self.updateSelectedRows()

    def setCurrentIndex(self, index: QModelIndex):
        QTableView.setCurrentIndex(self, index)
        self.updateSelectedRows()

    def updateSelectedRows(self):
        self._setSelectedRows(self.selectedIndexes())


class CustomTable(TableBase, QTableWidget):
    """ Table widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.verticalHeader().hide()

    def setCurrentCell(self, row: int, column: int, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        self.setCurrentItem(self.item(row, column), command)

    def setCurrentItem(self, item: QTableWidgetItem, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        if not command:
            super().setCurrentItem(item)
        else:
            super().setCurrentItem(item, command)

        self.updateSelectedRows()

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = pyqtProperty(bool, isSelectRightClickedRow, setSelectRightClickedRow)
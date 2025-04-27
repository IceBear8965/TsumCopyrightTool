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

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractItemView, QListView, QStyleOptionViewItem, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TableItemDelegate, themeColor, InfoBar, InfoBarPosition

from app.common.presetModel import presetModel
from app.common.saver import Saver
from app.common.setting import SETTING_FILE
from app.view.setup_interface.UI_SetupInterface import Ui_SetUpInterface


class ListItemDelegate(TableItemDelegate):
    """List item delegate"""

    def __init__(self, parent: QListView):
        super().__init__(parent)

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.drawRoundedRect(option.rect, 5, 5)

    def _drawIndicator(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        y, h = option.rect.y(), option.rect.height()
        ph = round(0.35 * h if self.pressedRow == index.row() else 0.257 * h)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(0, ph + y, 3, h - 2 * ph, 1.5, 1.5)

    def setActiveRow(self, index):
        self.selectedRows.clear()
        self.selectedRows.add(index.row())

    def removeActiveRow(self):
        self.selectedRows.clear()


class SetupInterface(Ui_SetUpInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("setupInterface")
        self.savePresetBtn.setIcon(FIF.SAVE)
        self.addPresetBtn.setIcon(FIF.ADD)
        self.delPresetBtn.setIcon(FIF.REMOVE)

        self.presetList.setModel(presetModel)
        self.presetList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.selectionModel = self.presetList.selectionModel()

        self.saver = Saver()
        # self.savedData = self.saver.load(SETTING_FILE)
        #
        # if not isinstance(self.savedData, bool) and not isinstance(self.savedData, list):
        #     presetModel.presetsData = self.savedData
        #
        # Visual selection of item in "current"
        if presetModel.getCurrentPreset() != "":
            self.presetList.setCurrentIndex(presetModel.index(presetModel.getCurrentPressetIndex()))
            self.setRelevantFields()
        # else:
        #     presetModel.presetsData = self.presetsData
        #     self.saver.save(SETTING_FILE, presetModel.presetsData)

        # connect signals to slots
        self.addPresetBtn.clicked.connect(self.addBtnHandler)
        self.delPresetBtn.clicked.connect(self.delBtnHandler)
        self.selectionModel.currentChanged.connect(self.changeSelectionHandler)
        self.savePresetBtn.clicked.connect(self.saveBtnHandler)

    def addBtnHandler(self):
        name = self.presetNameEdit.text()
        if len(name) != 0:
            presetModel.getPresetsObj().update(
                {
                    name: {
                        "filters": [],
                        "order": [],
                    }
                }
            )
            lastElement = presetModel.index(list(presetModel.getPresetsObj()).index(name))
            self.presetList.setCurrentIndex(lastElement)
            self.presetNameEdit.clear()
            presetModel.presetsData["current"] = name
            self.setRelevantFields()
            presetModel.layoutChanged.emit()

            self.saver.save(SETTING_FILE, presetModel.presetsData)
        else:
            InfoBar.warning(
                title="Add",
                content="Enter name in the field on the left",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )

    def delBtnHandler(self):
        if len(self.presetList.selectedIndexes()) > 0:
            if len(list(presetModel.getPresetsObj().keys())) > 1:
                selectedIndex = self.presetList.selectedIndexes()[0].row()
                presetModel.getPresetsObj().pop(list(presetModel.getPresetsObj().keys())[selectedIndex])
                presetModel.presetsData["current"] = ""
                self.filtersEdit.clear()
                self.orderEdit.clear()
                self.presetList.clearSelection()
                self.saver.save(SETTING_FILE, presetModel.presetsData)
                presetModel.layoutChanged.emit()
            else:
                InfoBar.warning(
                    title="Delete",
                    content="Cannot delete last preset",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title="Delete",
                content="Select preset which you want to delete",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )

    def changeSelectionHandler(self, selected):
        selectedIndex = selected.row()
        selectedElement = list(presetModel.getPresetsObj().keys())[selectedIndex]
        presetModel.presetsData["current"] = selectedElement
        self.presetList.setCurrentIndex(presetModel.index(selectedIndex))
        self.setRelevantFields()
        self.saver.save(SETTING_FILE, presetModel.presetsData)

        InfoBar.success(
            title="Change",
            content="Active preset changed",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=500,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

    def saveBtnHandler(self):
        try:
            preset = presetModel.getPresetsObj().get(presetModel.getCurrentPreset())
            filters = self.filtersEdit.toPlainText().split("\n")
            order = self.orderEdit.toPlainText().split("\n")

            filters = list(map(str.strip, filters))
            order = list(map(str.strip, order))

            for filter in filters:
                if filter == "":
                    filters.pop(filters.index(filter))
            for o in order:
                if o == "":
                    order.pop(order.index(o))

            preset["filters"] = filters
            preset["order"] = order
            self.saver.save(SETTING_FILE, presetModel.presetsData)
            InfoBar.success(
                title="Save",
                content="Preset saved successfully",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )
        except Exception:
            InfoBar.error(
                title="Error",
                content="An error occurred while recording the preset",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=2000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )

    def setRelevantFields(self):
        filters, order = presetModel.getSetting()
        filters = "\n".join(filters)
        order = "\n".join(order)

        self.filtersEdit.setPlainText(filters)
        self.orderEdit.setPlainText(order)

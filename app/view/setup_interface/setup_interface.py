'''
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
'''

from PyQt5.QtWidgets import QWidget, QAbstractItemView, QListView, QStyleOptionViewItem
from PyQt5.QtCore import Qt, QItemSelectionModel, QModelIndex
from PyQt5.QtGui import QPainter
from adodbapi.adodbapi import getIndexedValue
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition, TableItemDelegate, themeColor

from app.common.presetModel import presetModel
from app.common.saver import Saver
from app.common.setting import SETTING_FILE
from app.view.setup_interface.UI_SetupInterface import Ui_SetUpInterface


class ListItemDelegate(TableItemDelegate):
    """ List item delegate """

    def __init__(self, parent: QListView):
        super().__init__(parent)

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.drawRoundedRect(option.rect, 5, 5)

    def _drawIndicator(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        y, h = option.rect.y(), option.rect.height()
        ph = round(0.35*h if self.pressedRow == index.row() else 0.257*h)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(0, ph + y, 3, h - 2*ph, 1.5, 1.5)

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

        # adding model to ListView
        self.presetList.setModel(presetModel)
        self.presetList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.delegate = ListItemDelegate(self.presetList)
        self.presetList.setItemDelegate(self.delegate)
        self.selectionModel = self.presetList.selectionModel()

        # creating saver instance
        self.saver = Saver()

        # set default preset on load
        if len(presetModel.dataList[1]) != 0:
            self.filtersEdit.setPlainText(presetModel.getActivePreset()[1])
            self.orderEdit.setPlainText(presetModel.getActivePreset()[2])

            self.index = self.presetList.model().index(presetModel.getActiveIndex(), 0)
            self.delegate.setActiveRow(self.index)
            self.presetList.selectionModel().setCurrentIndex(self.index, QItemSelectionModel.SelectCurrent)

        # connect signal to slots
        self.addPresetBtn.clicked.connect(self.addPreset)
        self.delPresetBtn.clicked.connect(self.delPreset)
        self.savePresetBtn.clicked.connect(self.changePreset)
        self.selectionModel.selectionChanged.connect(self.onSelectionChanged)

    def addPreset(self):
        presetName = self.presetNameEdit.text()
        if presetName != "":
            presetModel.dataList[1].append([presetName, "", ""])

            self.delegate.setActiveRow(self.presetList.model().index(self.presetList.model().rowCount(presetModel.dataList[1])-1, 0))
            presetModel.setActiveIndex(presetModel.dataList[1].index(presetModel.dataList[1][-1]))

            key, filters, order = presetModel.getActivePreset()
            self.filtersEdit.setPlainText(filters)
            self.orderEdit.setPlainText(order)
            presetModel.layoutChanged.emit()

            self.presetNameEdit.clear()
            self.saver.save(presetModel.dataList, SETTING_FILE)

    def changePreset(self):
        try:
            filters = self.filtersEdit.toPlainText()
            order = self.orderEdit.toPlainText()
            index = presetModel.getActiveIndex()

            if filters and isinstance(index, int):
                presetModel.dataList[1][index][1] = filters
                presetModel.dataList[1][index][2] = order
                presetModel.layoutChanged.emit()

                self.saver.save(presetModel.dataList, SETTING_FILE)
            # Success info bar
            InfoBar.success(
                title='Save',
                content="Settings were saved successfully",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        except:
            InfoBar.error(
                title='Save',
                content="Settings were not saved",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    def delPreset(self):
        index = self.presetList.selectedIndexes()[0].row()
        presetModel.delPreset(index)
        self.delegate.removeActiveRow()

        activeRow = index - 1 if len(presetModel.dataList[1]) > 1 else 0
        presetModel.setActiveIndex(activeRow)

        self.filtersEdit.clear()
        self.orderEdit.clear()

        presetModel.layoutChanged.emit()
        self.saver.save(presetModel.dataList, SETTING_FILE)

    def onSelectionChanged(self):
        newSelectedItem = self.presetList.selectedIndexes()[0].row()
        presetModel.setActiveIndex(newSelectedItem)

        filters = presetModel.dataList[1][newSelectedItem][1]
        order = presetModel.dataList[1][newSelectedItem][2]
        self.filtersEdit.setPlainText(filters)
        self.orderEdit.setPlainText(order)

        self.saver.save(presetModel.dataList, SETTING_FILE)
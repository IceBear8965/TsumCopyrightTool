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

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractItemView, QListView, QStyleOptionViewItem, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TableItemDelegate, themeColor

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
        self.presetsData = {
            "current": "",
            "presets": {},
        }

        self.presetList.setModel(presetModel)
        self.presetList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.selectionModel = self.presetList.selectionModel()

        self.saver = Saver()
        self.savedData = self.saver.load(SETTING_FILE)

        if not isinstance(self.savedData, bool):
            presetModel.presetsData = self.savedData

            # Visual selection of item in "current"
            if presetModel.getCurrentPreset() != "":
                self.presetList.setCurrentIndex(
                    presetModel.index(  # Преобразовываем значение из int в QModelIndex
                        list(presetModel.getPresetsObj().keys()).index(
                            presetModel.getCurrentPreset()
                        )  # Получаем спискок из всех имен прессетов, находим нужный прессет по свойству из поля current
                    )
                )
                self.setRelevantFields()
        else:
            presetModel.presetsData = self.presetsData

    def setRelevantFields(self):
        preset = presetModel.getCurrentPreset()
        filters = presetModel.getPresetsObj().get(preset).get("filters")
        order = presetModel.getPresetsObj().get(preset).get("order")

        self.filtersEdit.setPlainText(filters)
        self.orderEdit.setPlainText(order)

        # connect signal to slots

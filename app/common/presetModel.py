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

from PyQt5.QtCore import QAbstractListModel, Qt


class PresetModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.presetsData = {}

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return list(self.presetsData.get("presets").keys())[index.row()]  # pyright: ignore

    def rowCount(self, index):
        return len(self.presetsData.get("presets").keys())  # pyright: ignore

    def getPresetsObj(self) -> dict:
        return self.presetsData.get("presets", dict())

    def getCurrentPreset(self) -> str:
        return self.presetsData.get("current", dict())

    def getCurrentPressetIndex(self):
        currentPressetIndex = list(self.getPresetsObj().keys()).index(self.getCurrentPreset())
        return currentPressetIndex

    def getSetting(self):
        filters = self.getPresetsObj().get(self.getCurrentPreset()).get("filters").split("\n")
        order = self.getPresetsObj().get(self.getCurrentPreset()).get("order").split("\n")
        filters = filters if filters[0] != "" else []
        order = order if order[0] != "" else []
        return filters, order


presetModel = PresetModel()

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


presetModel = PresetModel()

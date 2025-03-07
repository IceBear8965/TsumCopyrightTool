from PyQt5.QtCore import QAbstractListModel, Qt

class PresetModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataList = [0, []]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if len(self.dataList[1]) != 0:
                key, filters, order = self.dataList[1][index.row()]
                return key

    def rowCount(self, index):
        return len(self.dataList[1])

    def setActiveIndex(self, index):
        if index != self.dataList[0]:
            self.dataList[0] = index

    def getActiveIndex(self):
        return self.dataList[0]

    def getActivePreset(self):
        if len(self.dataList[1]) != 0:
            return self.dataList[1][self.getActiveIndex()]
        else:
            return []

    def getPresets(self):
        return self.dataList[1]

    def delPreset(self, index):
        self.dataList[1].pop(self.dataList[1].index(self.dataList[1][index]))

    def getParams(self):
        filters = self.dataList[self.activeIndex][1].split("\n")
        order = self.dataList[self.activeIndex][2].split("\n")

        return filters, order

presetModel = PresetModel()
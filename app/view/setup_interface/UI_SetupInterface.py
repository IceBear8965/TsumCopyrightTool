# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/view/uis/setup.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetUpInterface(object):
    def setupUi(self, SetUpInterface):
        SetUpInterface.setObjectName("SetUpInterface")
        SetUpInterface.resize(1000, 700)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SetUpInterface)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filtersEdit = PlainTextEdit(SetUpInterface)
        self.filtersEdit.setObjectName("filtersEdit")
        self.horizontalLayout.addWidget(self.filtersEdit)
        self.orderEdit = PlainTextEdit(SetUpInterface)
        self.orderEdit.setObjectName("orderEdit")
        self.horizontalLayout.addWidget(self.orderEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.saveSettingsBtn = PushButton(SetUpInterface)
        self.saveSettingsBtn.setObjectName("saveSettingsBtn")
        self.horizontalLayout_2.addWidget(self.saveSettingsBtn, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SetUpInterface)
        QtCore.QMetaObject.connectSlotsByName(SetUpInterface)

    def retranslateUi(self, SetUpInterface):
        _translate = QtCore.QCoreApplication.translate
        SetUpInterface.setWindowTitle(_translate("SetUpInterface", "Form"))
        self.filtersEdit.setPlaceholderText(_translate("SetUpInterface", "Filters"))
        self.orderEdit.setPlaceholderText(_translate("SetUpInterface", "Order"))
        self.saveSettingsBtn.setText(_translate("SetUpInterface", "Save"))
from qfluentwidgets import PlainTextEdit, PushButton


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SetUpInterface = QtWidgets.QWidget()
    ui = Ui_SetUpInterface()
    ui.setupUi(SetUpInterface)
    SetUpInterface.show()
    sys.exit(app.exec_())

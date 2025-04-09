# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/IceBear/projects/TsumCopyrightTool/app/view/uis/parse.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets  # noqa: F401


class Ui_ParseInterface(object):
    def setupUi(self, ParseInterface):
        ParseInterface.setObjectName("ParseInterface")
        ParseInterface.resize(1000, 700)
        ParseInterface.setStyleSheet("")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ParseInterface)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.webSiteNameCombo = ComboBox(ParseInterface)
        self.webSiteNameCombo.setObjectName("webSiteNameCombo")
        self.webSiteNameCombo.addItem("")
        self.webSiteNameCombo.addItem("")
        self.webSiteNameCombo.addItem("")
        self.webSiteNameCombo.addItem("")
        self.horizontalLayout_3.addWidget(self.webSiteNameCombo, 0, QtCore.Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(
            30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputUrl = LineEdit(ParseInterface)
        self.inputUrl.setObjectName("inputUrl")
        self.horizontalLayout.addWidget(self.inputUrl)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.parseBtn = PushButton(ParseInterface)
        self.parseBtn.setObjectName("parseBtn")
        self.horizontalLayout.addWidget(self.parseBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.parsedOutput = PlainTextEdit(ParseInterface)
        self.parsedOutput.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.parsedOutput.setObjectName("parsedOutput")
        self.verticalLayout_2.addWidget(self.parsedOutput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.copyParsedBtn = PushButton(ParseInterface)
        self.copyParsedBtn.setObjectName("copyParsedBtn")
        self.horizontalLayout_2.addWidget(self.copyParsedBtn, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(ParseInterface)
        QtCore.QMetaObject.connectSlotsByName(ParseInterface)

    def retranslateUi(self, ParseInterface):
        _translate = QtCore.QCoreApplication.translate
        ParseInterface.setWindowTitle(_translate("ParseInterface", "Form"))
        self.webSiteNameCombo.setItemText(0, _translate("ParseInterface", "Saks85"))
        self.webSiteNameCombo.setItemText(1, _translate("ParseInterface", "Saucony"))
        self.webSiteNameCombo.setItemText(2, _translate("ParseInterface", "Arena"))
        self.webSiteNameCombo.setItemText(3, _translate("ParseInterface", "Kidis"))
        self.inputUrl.setPlaceholderText(_translate("ParseInterface", "URL"))
        self.parseBtn.setText(_translate("ParseInterface", "Get Information"))
        self.parsedOutput.setPlaceholderText(_translate("ParseInterface", "Output"))
        self.copyParsedBtn.setText(_translate("ParseInterface", "Copy"))


from qfluentwidgets import ComboBox, LineEdit, PlainTextEdit, PushButton

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ParseInterface = QtWidgets.QWidget()
    ui = Ui_ParseInterface()
    ui.setupUi(ParseInterface)
    ParseInterface.show()
    sys.exit(app.exec_())

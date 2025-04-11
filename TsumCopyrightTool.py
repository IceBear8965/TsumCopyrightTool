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

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from app.view.main_window import MainWindow

# enable dpi scale

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

w = MainWindow()
w.show()
sys.exit(app.exec_())

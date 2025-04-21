from app.common.setting import WEBSITE_NAMES_LIST
from app.common.icon import CustomIcons
from qfluentwidgets import ComboBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


def set_websites_names(combo_box: ComboBox or QComboBox):
    for website_name in WEBSITE_NAMES_LIST:
        try:
            icon = CustomIcons[website_name]
            combo_box.addItem(website_name, icon)
        except Exception:
            combo_box.addItem(website_name)

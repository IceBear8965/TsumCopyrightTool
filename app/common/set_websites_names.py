from app.common.setting import WEBSITE_NAMES_LIST
from qfluentwidgets import ComboBox
from PyQt5.QtWidgets import QComboBox


def set_websites_names(combo_box: ComboBox or QComboBox):
    for website_name in WEBSITE_NAMES_LIST:
            combo_box.addItem(website_name)

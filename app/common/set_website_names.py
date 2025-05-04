from app.common.setting import WEBSITE_NAMES_LIST
from qfluentwidgets import ComboBox
from PyQt5.QtWidgets import QComboBox


def set_website_names(combo_box: ComboBox or QComboBox, values=WEBSITE_NAMES_LIST):
    for website_name in values:
            combo_box.addItem(website_name)

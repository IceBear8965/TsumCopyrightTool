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

from pathlib import Path

from PyQt5.QtCore import QStandardPaths

YEAR = 2025
AUTHOR = "IceBear8965"
VERSION = "0.0.1"
APP_NAME = "TsumCopyrightTool"
REPO_URL = "https://github.com/zhiyiYo/Fluent-M3U8"
RELEASE_URL = "https://github.com/zhiyiYo/Fluent-M3U8/releases"

CONFIG_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)) / APP_NAME
CONFIG_FILE = CONFIG_FOLDER / "config.json"
SETTING_FILE = CONFIG_FOLDER / "setting.json"

# List of websites that can be parsed
WEBSITE_NAMES_LIST = ["Saks85", "Saucony", "Arena", "Kidis"]

DOCUMENT_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))
DOWNLOAD_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))

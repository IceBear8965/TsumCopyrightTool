import sys
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

DOCUMENT_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))
DOWNLOAD_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))
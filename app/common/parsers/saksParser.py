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

import lxml  # noqa: F401
import requests
from bs4 import BeautifulSoup

from app.common.addDots import addDots
from app.common.sortInput import sortInput

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",  # noqa E501
}


def parseSaks(url, filters, order):
    html = requests.get(url, headers)
    src = html.text

    soup = BeautifulSoup(src, "lxml")

    htmlData = soup.find("div", class_="product__description").find_all("div")
    data = []

    # Проверка на пустые поля в <div></div>
    for d in htmlData:
        if len(d.text) > 2:
            data.append(d.text)

    for d in data:
        data.insert(data.index(d), data.pop(data.index(d)).replace("\r", "").replace("\n", ""))

    data = sortInput(data, filters, order)
    output = addDots(data)
    return output

'''
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
'''

import requests
from bs4 import BeautifulSoup
import lxml
from app.common.addDots import addDots

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def parseArena(url):
    src = requests.get(url, headers).text

    soup = BeautifulSoup(src, "lxml")

    specs = soup.find_all("div", class_="specifications-group")

    descriptionArrays = []
    description = []
    for spec in specs:
        paragraphs = spec.find_all("p")
        for p in paragraphs:
            value = p.text.strip().replace('\n', ' ').replace('\r', '')
            str = value.split()
            descriptionArrays.append(str)

    for d in descriptionArrays:
        str = " ".join(d)
        description.append(str)

    colour = ""
    colourIndex = 0
    for i in description:
        if "Колір:" in i:
            colour = i
            colourIndex = description.index(i)

    description.insert(0, colour)
    description.pop(colourIndex+1)

    for i in description:
        if "Стать:" in i:
            description.remove(i)

    def editStr(str):
        str = "• " + str
        return str

    output = addDots(description)
    return output
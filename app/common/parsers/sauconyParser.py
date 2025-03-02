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
def parseSaucony(url):
    src = requests.get(url, headers).text

    soup = BeautifulSoup(src, "lxml")
    table = soup.find("table", class_="table table-bordered").find_all("tbody")

    descriptionArr = []
    try:
        description = soup.find("div", id="dop_desc3").text
        description = description.strip().replace("\n", " ")
        descriptionArr = description.split(". ")
    except Exception:
        description = None

    string = ""
    paramsArr = []
    for t in table:
        tds = t.find_all("td")
        key = tds[0].text
        value = tds[1].text
        string = f"{key}: {value}"

        if "Стать:" not in string:
            paramsArr.append(string)


    data = paramsArr + descriptionArr
    output = addDots(data)
    return output
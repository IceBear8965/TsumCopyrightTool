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
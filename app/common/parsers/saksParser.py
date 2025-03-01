import requests
from bs4 import  BeautifulSoup
import lxml
from scripts.addDots import addDots
from scripts.sortInput import sortInput

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
def parseSaks(url, filters, order):
    html = requests.get(url, headers)
    src = html.text

    soup = BeautifulSoup(src, "lxml")

    htmlData = soup.find("div", class_="product__description").find_all("div")
    data = []

    for d in htmlData:
        if len(d.text) > 5:
            data.append(d.text)

    for d in data:
        data.insert(data.index(d), data.pop(data.index(d)).replace("\r", "").replace("\n", ""))

    data = sortInput(data, filters, order)
    output = addDots(data)
    return output
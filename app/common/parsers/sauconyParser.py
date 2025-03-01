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
import lxml  # noqa: F401
import requests  # noqa: F401
from bs4 import BeautifulSoup  # noqa: F401

from app.common.addDots import addDots  # noqa: F401
from app.common.sortInput import sortInput  # noqa: F401

headers = {
    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
}


def parseKidis(url, filters, order):
    html = requests.get(url, headers).text
    soup = BeautifulSoup(html, "lxml")
    features = soup.find("div", class_="accordion_item").find_all("li", class_="chars-list_item")

    data = []

    for feature in features:
        feature_name = feature.find("div", class_="chars-list_attr").text
        feature_value = feature.find("div", class_="chars-list_param").text

        feature_result = f"{feature_name}: {feature_value}"
        data.append(feature_result)

    data = sortInput(data, filters, order)
    output = addDots(data)
    return output

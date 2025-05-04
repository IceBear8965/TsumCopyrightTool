import requests
from bs4 import BeautifulSoup
import lxml

def fetch_saks_links(id):
    gen_url = f"https://saks85.com/search?search={id}"
    html = requests.get(gen_url).text
    soup = BeautifulSoup(html, "lxml")

    url = soup.find("div", class_="catalog-card__photo").find("a").get("href")
    return url

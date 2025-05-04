import requests
from bs4 import BeautifulSoup
import lxml

def fetch_kidis_links(id):
    gen_url = f"https://kidis.ua/search?value={id}"
    html = requests.get(gen_url).text
    soup = BeautifulSoup(html, "lxml")

    product_link = soup.find("a", class_="catalogItem_name").get("href")
    url = f"https://kidis.ua{product_link}"
    return url

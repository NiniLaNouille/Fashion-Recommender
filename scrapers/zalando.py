import requests
from bs4 import BeautifulSoup


def scrape():

    url = "https://www.zalando.fi/naiset-vaatteet/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    items = soup.select("article")

    for item in items[:20]:

        try:
            title = item.select_one("h3").text.strip()
            brand = item.select_one("h4").text.strip()
            price = item.select_one("span").text.strip()
            image = item.select_one("img")["src"]

            products.append({
                "id": title,
                "title": title,
                "brand": brand,
                "category": "unknown",
                "color": "",
                "price": price,
                "description": title,
                "image_url": image,
                "product_url": "",
                "source": "zalando"
            })

        except Exception:
            continue

    return products

import requests

def scrape():

    url = "https://api.zalando.com/articles?category=women&limit=20"

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    products = []

    for item in data.get("content", []):

        products.append({
            "id": item["id"],
            "title": item["name"],
            "brand": item["brand"]["name"],
            "category": item["category"],
            "color": item.get("color", ""),
            "price": item["price"]["value"],
            "description": item["name"],
            "image_url": item["media"]["images"][0]["smallUrl"],
            "product_url": item["shopUrl"],
            "source": "zalando"
        })

    return products

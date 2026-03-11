from scrapers.zalando import scrape


def run():

    products = scrape()

    print("Collected products:", len(products))

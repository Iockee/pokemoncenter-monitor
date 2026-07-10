import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.pokemoncenter.com/de-de/category/tcg-cards"


def get_page():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()
    return response.text


def get_products(html):
    soup = BeautifulSoup(html, "html.parser")

    products = []

    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            if data.get("@type") != "Product":
                continue

            products.append({
                "name": data.get("name"),
                "price": data.get("offers", {}).get("price"),
                "url": data.get("url"),
                "availability": data.get("offers", {}).get("availability"),
                "mpn": data.get("mpn")
            })

        except Exception:
            continue

    return products


def main():
    html = get_page()

    print("=" * 60)
    print(f"HTML Länge: {len(html)}")
    print("=" * 60)
    print(html[:1500])
    print("=" * 60)

    products = get_products(html)

    print(f"\n{len(products)} Produkte gefunden")

    for product in products:
        print("-" * 60)
        print(f"Name: {product['name']}")
        print(f"Preis: {product['price']}")
        print(f"Verfügbarkeit: {product['availability']}")
        print(f"URL: {product['url']}")
        print(f"MPN: {product['mpn']}")


if __name__ == "__main__":
    main()

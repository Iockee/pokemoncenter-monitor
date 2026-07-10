import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.pokemoncenter.com/de-de/category/tcg-cards"


def get_page():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        "Referer": "https://www.pokemoncenter.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.Session()

    response = session.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def get_products(html):
    soup = BeautifulSoup(html, "html.parser")

    products = []

    scripts = soup.find_all("script", type="application/ld+json")

    print(f"Gefundene JSON-LD Blöcke: {len(scripts)}")

    for script in scripts:
        try:
            if not script.string:
                continue

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

    if "Request unsuccessful" in html:
        print("❌ Imperva / Incapsula hat den Request blockiert.")
        return

    if "application/ld+json" in html:
        print("✅ JSON-LD Produktdaten gefunden.")
    else:
        print("❌ Keine JSON-LD Daten gefunden.")

    products = get_products(html)

    print(f"\n{len(products)} Produkte gefunden\n")

    for product in products:
        print("-" * 60)
        print(f"Name: {product['name']}")
        print(f"Preis: {product['price']}")
        print(f"Verfügbarkeit: {product['availability']}")
        print(f"URL: {product['url']}")


if __name__ == "__main__":
    main()

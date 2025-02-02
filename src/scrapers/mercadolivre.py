import requests
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper


class MercadoLivreScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://www.mercadolivre.com.br")

    def scrape_product_info(self, product_url):
        """Extracts product details such as name, price, and availability from Mercado Livre."""
        soup = self.fetch_page(product_url)
        if not soup:
            return None

        try:
            product_name = soup.find("h1", class_="ui-pdp-title").text.strip()
            product_price = soup.find("span", class_="andes-money-amount__fraction").text.strip()
            currency_symbol = soup.find("span", class_="andes-money-amount__currency-symbol").text.strip()
            availability = soup.find("span", class_="ui-pdp-stock__quantity").text.strip() if soup.find(
                "span", class_="ui-pdp-stock__quantity") else "Disponível"

            return {
                "name": product_name,
                "price": f"{currency_symbol} {product_price}",
                "availability": availability,
                "url": product_url
            }
        except AttributeError:
            print(f"Error extracting data from {product_url}")
            return None

    def scrape_multiple_products(self, search_query, max_results=10):
        """Scrapes multiple product listings from Mercado Livre search results."""
        search_url = f"{self.base_url}/jm/search?as_word={search_query.replace(' ', '+')}"

        soup = self.fetch_page(search_url)
        if not soup:
            return []

        products = []
        product_cards = soup.find_all("li", class_="ui-search-layout__item", limit=max_results)

        for card in product_cards:
            try:
                name = card.find("h2", class_="ui-search-item__title").text.strip()
                price = card.find("span", class_="andes-money-amount__fraction").text.strip()
                currency = card.find("span", class_="andes-money-amount__currency-symbol").text.strip()
                link = card.find("a", class_="ui-search-link")["href"]

                products.append({
                    "name": name,
                    "price": f"{currency} {price}",
                    "url": link
                })
            except AttributeError:
                continue

        return products

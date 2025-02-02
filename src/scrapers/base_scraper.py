import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import time
import random


class BaseScraper(ABC):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {"User-Agent": self.get_random_user_agent()}

    @staticmethod
    def get_random_user_agent():
        """Returns a random user agent from a predefined list."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        return random.choice(user_agents)

    def fetch_page(self, url):
        """Fetches a webpage and returns a BeautifulSoup object."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_product_info(self, product_url):
        """Extracts product details such as name, price, and availability."""
        soup = self.fetch_page(product_url)
        if soup:
            product_name = soup.find("span", class_="product-title")
            product_price = soup.find("span", class_="price")
            availability = soup.find("div", class_="availability")

            return {
                "name": product_name.text.strip() if product_name else "N/A",
                "price": product_price.text.strip() if product_price else "N/A",
                "availability": availability.text.strip() if availability else "N/A"
            }
        return None

    def scrape_multiple_products(self, search_query):
        """Scrapes multiple product listings from a search result page."""
        search_url = f"{self.base_url}/search?q={search_query}"
        soup = self.fetch_page(search_url)
        if soup:
            products = []
            product_cards = soup.find_all("div", class_="product-card")
            for card in product_cards:
                name = card.find("span", class_="product-title")
                price = card.find("span", class_="price")
                link = card.find("a", class_="product-link")

                products.append({
                    "name": name.text.strip() if name else "N/A",
                    "price": price.text.strip() if price else "N/A",
                    "link": link["href"] if link else "#"
                })
            return products
        return []

    def wait(self, min_time=1, max_time=3):
        """Waits a random time between requests to avoid detection."""
        time.sleep(random.uniform(min_time, max_time))

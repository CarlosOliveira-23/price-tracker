import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper


class AmazonScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://www.amazon.com.br")
        self.driver = self.init_driver()

    def init_driver(self):
        """Initialize the Selenium WebDriver."""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        service = Service(ChromeDriverManager().install())

        return webdriver.Chrome(service=service, options=chrome_options)

    def fetch_page(self, url):
        """Fetches a webpage using Selenium to bypass Amazon bot detection."""
        self.driver.get(url)
        try:
            (WebDriverWait(self.driver, 10).until
             (EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item"))))
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def scrape_product_info(self, product_url):
        """Extracts product details such as name, price, and availability from Amazon."""
        soup = self.fetch_page(product_url)
        if not soup:
            return None

        try:
            product_name = soup.select_one("#productTitle").text.strip()
            product_price = soup.select_one(".a-price .a-offscreen").text.strip() \
                if soup.select_one(".a-price .a-offscreen") else "N/A"
            availability = soup.select_one("#availability .a-declarative").text.strip() \
                if soup.select_one("#availability .a-declarative") else "Disponível"

            return {
                "name": product_name,
                "price": product_price,
                "availability": availability,
                "url": product_url
            }
        except AttributeError:
            print(f"Error extracting data from {product_url}")
            return None

    def scrape_multiple_products(self, search_query, max_results=10):
        """Scrapes multiple product listings from Amazon search results."""
        search_url = f"{self.base_url}/s?k={search_query.replace(' ', '+')}"
        self.driver.get(search_url)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located
                                                 ((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")))
        except Exception as e:
            print(f"Error loading search results: {e}")
            return []

        products = []
        product_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")

        for card in product_cards[:max_results]:
            try:
                name = (card.find_element(By.CSS_SELECTOR, "span.a-size-medium.a-color-base.a-text-normal").
                        text.strip())
                price = card.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip() \
                    if card.find_elements(By.CSS_SELECTOR, "span.a-price-whole") else "N/A"
                link = card.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")

                products.append({
                    "name": name,
                    "price": f"R$ {price}",
                    "url": link
                })
            except Exception:
                continue

        return products

    def close(self):
        """Close the Selenium driver."""
        self.driver.quit()

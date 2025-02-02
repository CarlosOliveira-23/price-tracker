from src.scrapers.amazon import AmazonScraper
from src.scrapers.mercadolivre import MercadoLivreScraper
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_scraper():
    print("📌 Welcome to Price Tracker!\n")
    print("Choose a platform to scrape:")
    print("1 - Mercado Livre")
    print("2 - Amazon")

    choice = input("\nEnter the number of your choice: ")

    if choice == "1":
        scraper = MercadoLivreScraper()
        platform = "Mercado Livre"
    elif choice == "2":
        scraper = AmazonScraper()
        platform = "Amazon"
    else:
        print("❌ Invalid choice. Exiting...")
        return

    search_query = input(f"\nEnter the product name to search on {platform}: ")
    print("\n🔍 Searching for products... Please wait.\n")

    products = scraper.scrape_multiple_products(search_query)

    if not products:
        print("❌ No products found.")
        return

    print(f"✅ {len(products)} products found on {platform}:\n")

    for index, product in enumerate(products, start=1):
        print(f"{index}. {product['name']}")
        print(f"   Price: {product['price']}")
        print(f"   URL: {product['url']}\n")

    choice = input("Do you want to get details of a specific product? (yes/no): ").strip().lower()

    if choice == "yes":
        product_index = int(input("\nEnter the product number: ")) - 1

        if 0 <= product_index < len(products):
            product_details = scraper.scrape_product_info(products[product_index]["url"])

            if product_details:
                print("\n🔎 Product Details:")
                print(f"Name: {product_details['name']}")
                print(f"Price: {product_details['price']}")
                print(f"Availability: {product_details['availability']}")
                print(f"URL: {product_details['url']}")
            else:
                print("❌ Unable to fetch product details.")
        else:
            print("❌ Invalid product number.")

    print("\n🎯 Scraping complete. Exiting program.")


if __name__ == "__main__":
    run_scraper()

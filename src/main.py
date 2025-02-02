import sys
import os
from src.scrapers.amazon import AmazonScraper
from src.scrapers.mercadolivre import MercadoLivreScraper
from src.data.data_cleaning import clean_product_data
from src.data.database import Database
from src.data.report_generator import generate_csv_report
from src.utils.logger import log_info, log_error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_scraper():
    """Runs the scraper, allowing the user to choose a platform and search for products."""
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

    try:
        products = scraper.scrape_multiple_products(search_query)
    except Exception as e:
        log_error(f"Error while scraping {platform}: {e}")
        print("❌ An error occurred during scraping.")
        return

    if not products:
        print("❌ No products found.")
        return

    print(f"✅ {len(products)} products found on {platform}:\n")

    cleaned_products = [clean_product_data(product) for product in products]

    for index, product in enumerate(cleaned_products, start=1):
        print(f"{index}. {product['name']}")
        print(f"   Price: {product['price']}")
        print(f"   URL: {product['url']}\n")

    db = Database()
    for product in cleaned_products:
        db.insert_product(product)

    db.close()
    log_info(f"Successfully stored {len(cleaned_products)} products from {platform} in the database.")

    generate_csv_report(cleaned_products, filename=f"{platform.replace(' ', '_')}_price_report.csv")
    log_info(f"CSV report generated for {platform}")

    choice = input("Do you want to get details of a specific product? (yes/no): ").strip().lower()

    if choice == "yes":
        product_index = int(input("\nEnter the product number: ")) - 1

        if 0 <= product_index < len(cleaned_products):
            try:
                product_details = scraper.scrape_product_info(cleaned_products[product_index]["url"])
            except Exception as e:
                log_error(f"Error while fetching product details: {e}")
                print("❌ Unable to fetch product details.")
                return

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

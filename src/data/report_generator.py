import csv


def generate_csv_report(products, filename="price_report.csv"):
    """Generates a CSV report with product data."""
    if not products:
        print("No data available to generate report.")
        return

    headers = ["Name", "Price", "URL", "Availability"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for product in products:
            writer.writerow([product["name"], product["price"], product["url"], product["availability"]])

    print(f"✅ Report generated: {filename}")

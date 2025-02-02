import re


def clean_price(price):
    """Cleans and converts a price string into a float."""
    if not price:
        return 0.0
    price = re.sub(r"[^\d,]", "", price)  # Remove caracteres indesejados
    price = price.replace(",", ".")  # Troca vírgula por ponto
    return float(price) if price else 0.0


def normalize_text(text):
    """Removes extra spaces and converts text to lowercase."""
    return text.strip().lower() if text else ""


def clean_product_data(product):
    """Cleans product data fields."""
    return {
        "name": normalize_text(product.get("name", "")),
        "price": clean_price(product.get("price", "0")),
        "url": product.get("url", ""),
        "availability": normalize_text(product.get("availability", ""))
    }

# 🏷️ Price Tracker

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup%20%7C%20Selenium-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A web scraper that collects competitor prices from **Amazon** and **Mercado Livre**, generating comparative reports for e-commerce businesses. Built with **Python, BeautifulSoup, Selenium, and Pandas**.

---

## 🚀 Features
✅ Scrapes product prices from Amazon and Mercado Livre  
✅ Cleans and standardizes data before saving  
✅ Stores product details in a **SQLite database**  
✅ Generates **CSV reports** for easy analysis  
✅ Logs activity for debugging and tracking  

---

## 📦 Installation

First, **clone this repository** and navigate to the project directory:

    ```bash
    git clone https://github.com/YOUR_USERNAME/price-tracker.git
    cd price-tracker


    1️⃣  ️⃣ Create a virtual environment:
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # OR
    .venv\Scripts\activate  # Windows


    2️⃣ Install dependencies:
    pip install -r requirements.txt


    3️⃣ Run the scraper:
    python -m src.main

---

## 🖥️ Usage
After running the scraper, choose the platform:

📌 Welcome to Price Tracker!

Choose a platform to scrape:
1 - Mercado Livre
2 - Amazon

Then, enter the product name:
Enter the product name to search on Amazon: Keyboard Logitech

✅ Sample Output:
🔍 Searching for products... Please wait.

✅ 10 products found on Amazon:

1. Logitech MX Keys Wireless Keyboard
   Price: R$ 529.90
   URL: https://www.amazon.com.br/dp/B085LNZK47

2. Logitech G PRO X Gaming Keyboard
   Price: R$ 699.90
   URL: https://www.amazon.com.br/dp/B081TLYV5P

📊 Reports & Database
All products are saved in a SQLite database (scraper_data.db)
A CSV report (Amazon_price_report.csv) is generated after scraping

🤝 Contributing
If you want to improve this project:

1. Fork this repository
2. Create a new branch: git checkout -b feature-new-feature
3. Commit your changes: git commit -m ":sparkles: feat: Added new feature"
4. Push to your branch: git push origin feature-new-feature
5. Open a Pull Request 🚀
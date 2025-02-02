import sqlite3


class Database:
    def __init__(self, db_name="scraper_data.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Creates the product table if it does not exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                url TEXT,
                availability TEXT
            )
        """)
        self.connection.commit()

    def insert_product(self, product):
        """Inserts a product into the database."""
        self.cursor.execute("""
            INSERT INTO products (name, price, url, availability)
            VALUES (?, ?, ?, ?)
        """, (product["name"], product["price"], product["url"], product["availability"]))
        self.connection.commit()

    def close(self):
        """Closes the database connection."""
        self.connection.close()

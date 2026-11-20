
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "restaurant.db"


def get_connection():

    DB_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():

    conn = get_connection()

    try:

        conn.executescript("""

        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            is_available INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_type TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL DEFAULT 0,
            tax_rate REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            grand_total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            item_total REAL NOT NULL,

            FOREIGN KEY(order_id)
            REFERENCES orders(order_id),

            FOREIGN KEY(item_id)
            REFERENCES menu_items(item_id)
        );

        """)

        sample_items = [
            ("Veg Burger", "Fast Food", 80),
            ("Pizza", "Fast Food", 200),
            ("Sandwich", "Snacks", 60),
            ("Cold Coffee", "Drinks", 90),
            ("French Fries", "Snacks", 100)
        ]

        conn.executemany("""
            INSERT OR IGNORE INTO menu_items
            (item_name, category, price)
            VALUES (?, ?, ?)
        """, sample_items)

        conn.commit()

        print("Database created successfully!")

    except sqlite3.Error as e:

        print("Database Error:", e)
        conn.rollback()

    finally:

        conn.close()


if __name__ == "__main__":
    initialize_database()

import sqlite3

def create_database():
    conn = sqlite3.connect("store.db")

    # ── Products Table ────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id       INTEGER PRIMARY KEY,
            name     TEXT,
            size     TEXT,
            color    TEXT,
            quantity INTEGER,
            price    REAL
        )
    """)

    # ── Orders Table ──────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id            INTEGER PRIMARY KEY,
            customer_name TEXT,
            customer_email TEXT,
            product_id    INTEGER,
            quantity      INTEGER,
            total_price   REAL,
            status        TEXT,
            date          TEXT
        )
    """)

    # ── Notifications Table ───────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id        INTEGER PRIMARY KEY,
            type      TEXT,
            message   TEXT,
            email     TEXT,
            timestamp TEXT,
            status    TEXT
        )
    """)

    # ── Fake Products Data ────────────────────────────────────
    products = [
        ("Blue T-Shirt",    "S",   "Blue",  10, 19.99),
        ("Blue T-Shirt",    "M",   "Blue",   5, 19.99),
        ("Blue T-Shirt",    "L",   "Blue",   0, 19.99),
        ("Blue T-Shirt",    "XL",  "Blue",   8, 19.99),
        ("Black Hoodie",    "M",   "Black", 15, 49.99),
        ("Black Hoodie",    "L",   "Black",  3, 49.99),
        ("Black Hoodie",    "XL",  "Black",  0, 49.99),
        ("White Sneakers",  "42",  "White",  7, 89.99),
        ("White Sneakers",  "43",  "White",  2, 89.99),
        ("White Sneakers",  "44",  "White",  0, 89.99),
        ("Red Jacket",      "S",   "Red",    4, 79.99),
        ("Red Jacket",      "M",   "Red",    6, 79.99),
        ("Red Jacket",      "L",   "Red",    0, 79.99),
        ("Black Jeans",     "32",  "Black",  5, 59.99),
        ("Black Jeans",     "34",  "Black",  3, 59.99),
        ("Black Jeans",     "36",  "Black",  8, 59.99),
    ]

    conn.executemany(
        "INSERT INTO products (name, size, color, quantity, price) VALUES (?,?,?,?,?)",
        products
    )

    conn.commit()
    conn.close()
    print("Database created successfully!")
    print("Tables: products, orders, notifications")
    print(f"Inserted {len(products)} products")


if __name__ == "__main__":
    create_database()
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "sales.db"

REGIONS = ["South", "North", "West", "East"]
CITIES = ["Hyderabad", "Bengaluru", "Chennai", "Delhi", "Mumbai", "Pune"]
SEGMENTS = ["Consumer", "SMB", "Enterprise"]
CATEGORIES = ["Electronics", "Accessories", "Home", "Books"]
CHANNELS = ["Online", "Retail", "Partner"]

def create_schema(conn: sqlite3.Connection):
    cur = conn.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        segment TEXT NOT NULL
    );
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        list_price REAL NOT NULL
    );
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,          -- ISO date (YYYY-MM-DD)
        channel TEXT NOT NULL,
        region TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        discount REAL NOT NULL,            -- 0.0 to 0.5
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    CREATE INDEX idx_orders_date ON orders(order_date);
    CREATE INDEX idx_orders_region ON orders(region);
    CREATE INDEX idx_products_category ON products(category);
    CREATE INDEX idx_order_items_order ON order_items(order_id);
    """)

    conn.commit()

def seed_data(conn: sqlite3.Connection,
              n_customers=200,
              n_products=60,
              n_orders=2000,
              max_items_per_order=5,
              days_back=365):
    cur = conn.cursor()
    random.seed(42)

    # Customers
    customers = []
    for cid in range(1, n_customers + 1):
        customers.append((
            cid,
            f"Customer {cid:04d}",
            random.choice(CITIES),
            random.choice(SEGMENTS),
        ))
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?);", customers)

    # Products
    products = []
    for pid in range(1, n_products + 1):
        cat = random.choice(CATEGORIES)
        base = {
            "Electronics": random.uniform(3000, 40000),
            "Accessories": random.uniform(200, 5000),
            "Home": random.uniform(500, 15000),
            "Books": random.uniform(150, 1500),
        }[cat]
        products.append((
            pid,
            f"Product {pid:03d}",
            cat,
            round(base, 2),
        ))
    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?);", products)

    # Orders + Order items
    start_date = datetime.today() - timedelta(days=days_back)

    order_rows = []
    item_rows = []
    order_item_id = 1

    for oid in range(1, n_orders + 1):
        cust_id = random.randint(1, n_customers)
        dt = start_date + timedelta(days=random.randint(0, days_back))
        order_date = dt.strftime("%Y-%m-%d")
        channel = random.choice(CHANNELS)
        region = random.choice(REGIONS)

        order_rows.append((oid, cust_id, order_date, channel, region))

        n_items = random.randint(1, max_items_per_order)
        chosen_products = random.sample(range(1, n_products + 1), k=n_items)

        for pid in chosen_products:
            qty = random.randint(1, 6)
            # Get list price
            list_price = next(p[3] for p in products if p[0] == pid)
            # Simulate price variation + discount
            unit_price = round(list_price * random.uniform(0.85, 1.05), 2)
            discount = round(random.choice([0, 0.05, 0.1, 0.15, 0.2]), 2)

            item_rows.append((
                order_item_id, oid, pid, qty, unit_price, discount
            ))
            order_item_id += 1

    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?);", order_rows)
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?);", item_rows)

    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)
    seed_data(conn)
    conn.close()
    print(f"✅ Created and seeded {DB_PATH}")

if __name__ == "__main__":
    main()
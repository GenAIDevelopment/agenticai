import csv
import random
from datetime import datetime, timedelta

# Output CSV files
CUSTOMERS_CSV = "customers.csv"
PRODUCTS_CSV = "products.csv"
ORDERS_CSV = "orders.csv"
ORDER_ITEMS_CSV = "order_items.csv"

REGIONS = ["South", "North", "West", "East"]
CITIES = ["Hyderabad", "Bengaluru", "Chennai", "Delhi", "Mumbai", "Pune"]
SEGMENTS = ["Consumer", "SMB", "Enterprise"]
CATEGORIES = ["Electronics", "Accessories", "Home", "Books"]
CHANNELS = ["Online", "Retail", "Partner"]

def seed_data(
    n_customers=200,
    n_products=60,
    n_orders=2000,
    max_items_per_order=5,
    days_back=365
):
    random.seed(42)

    # ----------------------
    # Customers
    # ----------------------
    customers = []
    for cid in range(1, n_customers + 1):
        customers.append([
            cid,
            f"Customer {cid:04d}",
            random.choice(CITIES),
            random.choice(SEGMENTS),
        ])

    # ----------------------
    # Products
    # ----------------------
    products = []
    for pid in range(1, n_products + 1):
        category = random.choice(CATEGORIES)
        base_price = {
            "Electronics": random.uniform(3000, 40000),
            "Accessories": random.uniform(200, 5000),
            "Home": random.uniform(500, 15000),
            "Books": random.uniform(150, 1500),
        }[category]

        products.append([
            pid,
            f"Product {pid:03d}",
            category,
            round(base_price, 2),
        ])

    product_price_map = {p[0]: p[3] for p in products}

    # ----------------------
    # Orders & Order Items
    # ----------------------
    orders = []
    order_items = []
    order_item_id = 1

    start_date = datetime.today() - timedelta(days=days_back)

    for oid in range(1, n_orders + 1):
        customer_id = random.randint(1, n_customers)
        order_date = (
            start_date + timedelta(days=random.randint(0, days_back))
        ).strftime("%Y-%m-%d")

        channel = random.choice(CHANNELS)
        region = random.choice(REGIONS)

        orders.append([
            oid,
            customer_id,
            order_date,
            channel,
            region,
        ])

        n_items = random.randint(1, max_items_per_order)
        chosen_products = random.sample(range(1, n_products + 1), n_items)

        for pid in chosen_products:
            qty = random.randint(1, 6)
            list_price = product_price_map[pid]
            unit_price = round(list_price * random.uniform(0.85, 1.05), 2)
            discount = round(random.choice([0, 0.05, 0.1, 0.15, 0.2]), 2)

            order_items.append([
                order_item_id,
                oid,
                pid,
                qty,
                unit_price,
                discount,
            ])
            order_item_id += 1

    return customers, products, orders, order_items

def write_csv(filename, header, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def main():
    customers, products, orders, order_items = seed_data()

    write_csv(
        CUSTOMERS_CSV,
        ["customer_id", "name", "city", "segment"],
        customers,
    )

    write_csv(
        PRODUCTS_CSV,
        ["product_id", "name", "category", "list_price"],
        products,
    )

    write_csv(
        ORDERS_CSV,
        ["order_id", "customer_id", "order_date", "channel", "region"],
        orders,
    )

    write_csv(
        ORDER_ITEMS_CSV,
        ["order_item_id", "order_id", "product_id", "qty", "unit_price", "discount"],
        order_items,
    )

    print("✅ CSV files created:")
    print(f" - {CUSTOMERS_CSV}")
    print(f" - {PRODUCTS_CSV}")
    print(f" - {ORDERS_CSV}")
    print(f" - {ORDER_ITEMS_CSV}")

if __name__ == "__main__":
    main()

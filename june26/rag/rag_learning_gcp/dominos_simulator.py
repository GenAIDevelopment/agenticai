
#!/usr/bin/env python3
"""
Domino's Sales Simulator (SQLite)

Usage:

Create a new database with historical data
------------------------------------------
python dominos_simulator.py init

Generate one live order every 2 seconds
---------------------------------------
python dominos_simulator.py live

Generate one live order every second
------------------------------------
python dominos_simulator.py live --interval 1

Generate 100 live orders immediately
------------------------------------
python dominos_simulator.py batch --count 100
"""

import argparse
import random
import sqlite3
import time
from datetime import datetime, timedelta

DB_NAME="dominos_sales.db"
random.seed()

CITIES=[
"Hyderabad","Bengaluru","Chennai","Mumbai","Delhi","Pune",
"Ahmedabad","Kolkata","Jaipur","Lucknow","Visakhapatnam","Bhopal"
]

PIZZAS=[
("Margherita","Veg",199),
("Farmhouse","Veg",329),
("Veg Extravaganza","Veg",399),
("Paneer Makhani","Veg",359),
("Peppy Paneer","Veg",349),
("Chicken Dominator","Non Veg",499),
("Pepper Barbecue Chicken","Non Veg",449),
("Chicken Golden Delight","Non Veg",429),
("Chicken Fiesta","Non Veg",379),
("Mexican Green Wave","Veg",349)
]

FN=["Amit","Rahul","Sneha","Priya","Ankit","Rohit","Meera","Kiran","Lakshmi","Arjun","Suresh","Nikhil","Pooja","Neha","Harsha","Divya"]
LN=["Sharma","Reddy","Patel","Singh","Kumar","Gupta","Iyer","Nair","Das","Verma","Rao"]

PAY=["UPI","Cash","Credit Card","Debit Card","Net Banking"]
DELIVERY=["Delivery","Takeaway","Dine-In"]

def conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    con=conn(); cur=con.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS branches;
    DROP TABLE IF EXISTS pizzas;
    DROP TABLE IF EXISTS cities;
    CREATE TABLE cities(city_id INTEGER PRIMARY KEY,city_name TEXT);
    CREATE TABLE branches(branch_id INTEGER PRIMARY KEY,city_id INTEGER,branch_name TEXT,manager_name TEXT);
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT,city_id INTEGER);
    CREATE TABLE pizzas(pizza_id INTEGER PRIMARY KEY,pizza_name TEXT,category TEXT,base_price REAL);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY,customer_id INTEGER,branch_id INTEGER,order_date TEXT,payment_method TEXT,delivery_type TEXT);
    CREATE TABLE order_items(item_id INTEGER PRIMARY KEY,order_id INTEGER,pizza_id INTEGER,quantity INTEGER,unit_price REAL);
    """)
    for c in CITIES:
        cur.execute("INSERT INTO cities(city_name) VALUES(?)",(c,))
    bid=1
    for city in range(1,len(CITIES)+1):
        for i in range(random.randint(2,4)):
            cur.execute("INSERT INTO branches VALUES(?,?,?,?)",
                        (bid,city,f"Dominos Branch {i+1}",random.choice(FN)+" "+random.choice(LN)))
            bid+=1
    for p in PIZZAS:
        cur.execute("INSERT INTO pizzas(pizza_name,category,base_price) VALUES(?,?,?)",p)
    cid=1
    for city in range(1,len(CITIES)+1):
        for _ in range(100):
            cur.execute("INSERT INTO customers VALUES(?,?,?)",
                        (cid,random.choice(FN)+" "+random.choice(LN),city))
            cid+=1
    start=datetime(2024,1,1)
    oid=1
    iid=1
    for _ in range(10000):
        cust=random.randint(1,cid-1)
        city=cur.execute("SELECT city_id FROM customers WHERE customer_id=?",(cust,)).fetchone()[0]
        branch=random.choice([r[0] for r in cur.execute("SELECT branch_id FROM branches WHERE city_id=?",(city,)).fetchall()])
        dt=start+timedelta(days=random.randint(0,364),hours=random.randint(10,22),minutes=random.randint(0,59))
        cur.execute("INSERT INTO orders VALUES(?,?,?,?,?,?)",
                    (oid,cust,branch,dt.strftime("%Y-%m-%d %H:%M:%S"),random.choice(PAY),random.choice(DELIVERY)))
        ids=random.sample(range(1,len(PIZZAS)+1),random.randint(1,4))
        for pid in ids:
            price=cur.execute("SELECT base_price FROM pizzas WHERE pizza_id=?",(pid,)).fetchone()[0]
            cur.execute("INSERT INTO order_items VALUES(?,?,?,?,?)",
                        (iid,oid,pid,random.randint(1,3),round(price*random.uniform(.9,1.1),2)))
            iid+=1
        oid+=1
    con.commit()
    con.close()
    print("Database initialized.")

def insert_order():
    con=conn(); cur=con.cursor()
    oid=cur.execute("SELECT COALESCE(MAX(order_id),0)+1 FROM orders").fetchone()[0]
    iid=cur.execute("SELECT COALESCE(MAX(item_id),0)+1 FROM order_items").fetchone()[0]
    cust,city=cur.execute("SELECT customer_id,city_id FROM customers ORDER BY RANDOM() LIMIT 1").fetchone()
    branch=cur.execute("SELECT branch_id FROM branches WHERE city_id=? ORDER BY RANDOM() LIMIT 1",(city,)).fetchone()[0]
    cur.execute("INSERT INTO orders VALUES(?,?,?,?,?,?)",
                (oid,cust,branch,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),random.choice(PAY),random.choice(DELIVERY)))
    pizzas=cur.execute("SELECT pizza_id,base_price FROM pizzas").fetchall()
    for pid,price in random.sample(pizzas,random.randint(1,4)):
        cur.execute("INSERT INTO order_items VALUES(?,?,?,?,?)",
                    (iid,oid,pid,random.randint(1,3),round(price*random.uniform(.9,1.1),2)))
        iid+=1
    con.commit()
    con.close()
    print(f"Inserted order {oid} @ {datetime.now():%H:%M:%S}")

def live(interval):
    print("Press Ctrl+C to stop.")
    try:
        while True:
            hour=datetime.now().hour
            if 11<=hour<=14:
                wait=random.uniform(.5,2)
            elif 18<=hour<=22:
                wait=random.uniform(.3,1.5)
            elif 15<=hour<=17:
                wait=random.uniform(2,5)
            else:
                wait=interval
            insert_order()
            time.sleep(wait)
    except KeyboardInterrupt:
        print("Stopped.")

def batch(count):
    for _ in range(count):
        insert_order()

def main():
    ap=argparse.ArgumentParser(description="Domino's SQLite Sales Simulator")
    sub=ap.add_subparsers(dest="cmd",required=True)

    sub.add_parser("init")
    l=sub.add_parser("live")
    l.add_argument("--interval",type=float,default=5.0)
    b=sub.add_parser("batch")
    b.add_argument("--count",type=int,default=100)

    args=ap.parse_args()

    if args.cmd=="init":
        init_db()
    elif args.cmd=="live":
        live(args.interval)
    elif args.cmd=="batch":
        batch(args.count)

if __name__=="__main__":
    main()

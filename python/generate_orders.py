import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("data/shopsphere.db")
cursor = conn.cursor()

# get all customer_ids
cursor.execute("SELECT customer_id FROM customers")
customers = [row[0] for row in cursor.fetchall()]

# get all product_ids and prices
cursor.execute("SELECT product_id, price FROM products")
products = cursor.fetchall()

order_id = 1
start_date = datetime(2023, 1, 1)

for _ in range(3000):
    customer_id = random.choice(customers)
    product_id, price = random.choice(products)

    quantity = random.randint(1, 4)
    discount = random.choice([0, 0, 0.1, 0.2])  # mostly no discount
    revenue = quantity * price * (1 - discount)

    order_date = start_date + timedelta(days=random.randint(0, 365))

    cursor.execute("""
        INSERT INTO orders (
            order_id, customer_id, product_id,
            order_date, quantity, discount, revenue
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        customer_id,
        product_id,
        order_date.strftime("%Y-%m-%d"),
        quantity,
        discount,
        revenue
    ))

    order_id += 1

conn.commit()
conn.close()

import sqlite3
import random

conn = sqlite3.connect("data/shopsphere.db")
cursor = conn.cursor()

products = [
    ("Bluetooth Speaker", "Electronics"),
    ("Wireless Headphones", "Electronics"),
    ("Smart Watch", "Electronics"),
    ("Running Shoes", "Fashion"),
    ("Leather Wallet", "Fashion"),
    ("Denim Jacket", "Fashion"),
    ("Face Serum", "Beauty"),
    ("Lipstick", "Beauty"),
    ("Sunscreen", "Beauty"),
    ("Perfume", "Beauty")
]

product_id = 1

for name, category in products:
    for _ in range(6):  # create variations
        price = random.randint(500, 5000)
        cost = int(price * random.uniform(0.5, 0.75))

        cursor.execute("""
            INSERT INTO products (product_id, product_name, category, price, cost)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_id,
            f"{name} {product_id}",
            category,
            price,
            cost
        ))

        product_id += 1

conn.commit()
conn.close()

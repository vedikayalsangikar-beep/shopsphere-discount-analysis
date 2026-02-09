import sqlite3
import random
from datetime import datetime, timedelta
# connect to database
conn = sqlite3.connect("data/shopsphere.db")
cursor = conn.cursor()

cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad"]
genders = ["Male", "Female"]
income_bands = ["Low", "Mid", "High"]

start_date = datetime(2022, 1, 1)

for i in range(6, 506):
    age = random.randint(18, 60)
    gender = random.choice(genders)
    city = random.choice(cities)
    income = random.choice(income_bands)
    signup_date = start_date + timedelta(days=random.randint(0, 600))

    cursor.execute("""
        INSERT INTO customers (customer_id, age, gender, city, income_band, signup_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        i,
        age,
        gender,
        city,
        income,
        signup_date.strftime("%Y-%m-%d")
    ))

conn.commit()
conn.close()

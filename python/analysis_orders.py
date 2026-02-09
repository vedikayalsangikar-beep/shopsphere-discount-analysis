import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect("data/shopsphere.db")

# pull joined dataset
query = """
SELECT
    o.order_id,
    o.order_date,
    o.quantity,
    o.discount,
    o.revenue,
    p.price,
    p.category,
    c.income_band,
    c.age,
    c.gender
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
"""

df = pd.read_sql(query, conn)

conn.close()

print(df.head())
print(df.shape)

import statsmodels.formula.api as smf

# treat categorical variables explicitly
df["income_band"] = df["income_band"].astype("category")
df["gender"] = df["gender"].astype("category")

# simple regression model
model = smf.ols(
    formula="""
    revenue ~ price + quantity + discount + C(income_band) + age + C(gender)
    """,
    data=df
).fit()

print(model.summary())

import matplotlib.pyplot as plt

plt.figure()
plt.scatter(df["discount"], df["revenue"])
plt.xlabel("Discount")
plt.ylabel("Revenue")
plt.title("Revenue vs Discount")
plt.show()
import matplotlib.pyplot as plt

plt.figure()
plt.scatter(df["discount"], df["revenue"])
plt.xlabel("Discount")
plt.ylabel("Revenue")
plt.title("Revenue vs Discount")
plt.show()

# ---- Export data for Tableau ----
df.to_csv("data/orders_analysis.csv", index=False)
print("orders_analysis.csv created successfully")

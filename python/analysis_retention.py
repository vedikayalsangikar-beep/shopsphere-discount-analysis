import sqlite3
import pandas as pd

conn = sqlite3.connect(
    r"C:\Users\Vedika\OneDrive\Desktop\shopsphere-project\data\shopsphere.db"
)

df = pd.read_sql("SELECT * FROM customer_summary", conn)

print("Shape:", df.shape)
print(df.head())

result = (
    df
    .groupby("discount_bucket")
    .agg(
        repeat_rate=("is_repeat_customer", "mean"),
        avg_orders_per_customer=("order_count", "mean"),
        avg_revenue=("total_revenue", "mean")
    )
    .reset_index()
)

print("\nRetention Summary:")
print(result)
import matplotlib.pyplot as plt

result.plot(
    x="discount_bucket",
    y="repeat_rate",
    kind="bar",
    legend=False,
    title="Repeat Rate by Discount Bucket"
)
plt.ylabel("Repeat Rate")
plt.show()

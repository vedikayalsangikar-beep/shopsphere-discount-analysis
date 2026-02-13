import pandas as pd
import numpy as np
import sqlite3
from scipy.stats import ttest_ind

# Connect to DB
conn = sqlite3.connect("data/shopsphere.db")

# Load early behavior
early = pd.read_sql("SELECT * FROM customer_early_behavior", conn)

# Load lifetime summary
lifetime = pd.read_sql("""
    SELECT customer_id, total_revenue
    FROM customer_summary
""", conn)

# Merge
df = early.merge(lifetime, on="customer_id")

print("Shape:", df.shape)
df.head()

# Define high-value cutoff (top 25%)
cutoff = df["total_revenue"].quantile(0.75)

df["high_value_customer"] = (
    df["total_revenue"] >= cutoff
).astype(int)

print("High-value cutoff:", cutoff)
print(df["high_value_customer"].value_counts())

metrics = [
    "orders_first_30_days",
    "revenue_first_30_days",
    "avg_discount_first_30_days"
]

results = []

for metric in metrics:
    high_group = df[df["high_value_customer"] == 1][metric]
    low_group = df[df["high_value_customer"] == 0][metric]
    
    mean_high = high_group.mean()
    mean_low = low_group.mean()
    
    lift_pct = ((mean_high - mean_low) / mean_low) * 100
    
    t_stat, p_value = ttest_ind(high_group, low_group)
    
    results.append({
        "Metric": metric,
        "High_Value_Mean": mean_high,
        "Low_Value_Mean": mean_low,
        "Lift_%": lift_pct,
        "P_Value": p_value
    })

signal_df = pd.DataFrame(results)

print(signal_df)

# ---- Export data for Tableau ----
signal_df.to_csv("data/model4_signal_summary.csv", index=False)

df.to_csv("data/model4_customer_features.csv", index=False)
print("Exported model4_customer_features.csv")

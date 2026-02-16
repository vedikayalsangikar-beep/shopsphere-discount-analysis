import pandas as pd
import numpy as np
import sqlite3


conn = sqlite3.connect(
    r"C:\Users\Vedika\OneDrive\Desktop\shopsphere-project\data\shopsphere.db"
)

df = pd.read_sql("SELECT * FROM model5_segmentation_base", conn)

print("Base shape:", df.shape)

cutoff = df["total_revenue"].quantile(0.75)

df["high_value_customer"] = (
    df["total_revenue"] >= cutoff
).astype(int)

print("\nHigh-value cutoff:", cutoff)
print(df["high_value_customer"].value_counts())


df["orders_per_day"] = df["order_count"] / (df["days_active"] + 1)

df["early_revenue_ratio"] = (
    df["revenue_first_30_days"] / df["total_revenue"]
)

df["discount_gap"] = (
    df["avg_discount_first_30_days"] - df["avg_discount_lifetime"]
)

df = df.replace([np.inf, -np.inf], 0).fillna(0)

discount_median = df["avg_discount_lifetime"].median()

print("\nMedian lifetime discount:", discount_median)

def assign_segment(row):
    if row["high_value_customer"] == 1 and row["avg_discount_lifetime"] <= discount_median:
        return "Premium Core"
    elif row["high_value_customer"] == 1 and row["avg_discount_lifetime"] > discount_median:
        return "Incentive Driven High Value"
    elif row["high_value_customer"] == 0 and row["avg_discount_lifetime"] > discount_median:
        return "Discount Dependent"
    else:
        return "Low Engagement"


df["strategic_segment"] = df.apply(assign_segment, axis=1)

print("\nSegment Distribution:")
print(df["strategic_segment"].value_counts())

segment_summary = df.groupby("strategic_segment").agg(
    customers=("customer_id", "count"),
    avg_revenue=("total_revenue", "mean"),
    avg_discount=("avg_discount_lifetime", "mean"),
    avg_orders=("order_count", "mean")
).reset_index()

segment_summary["revenue_contribution_%"] = (
    df.groupby("strategic_segment")["total_revenue"].sum()
    / df["total_revenue"].sum()
).values * 100


print("\nSegment Performance Summary:")
print(segment_summary)

cluster_features = [
    "total_revenue",
    "order_count",
    "avg_order_value",
    "avg_discount_lifetime",
    "revenue_first_30_days",
    "orders_first_30_days"
]

X = df[cluster_features].copy()

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

print("\nCluster Distribution:")
print(df["cluster"].value_counts())

cluster_summary = df.groupby("cluster").agg(
    customers=("customer_id", "count"),
    avg_revenue=("total_revenue", "mean"),
    avg_orders=("order_count", "mean"),
    avg_discount=("avg_discount_lifetime", "mean")
).reset_index()

cluster_summary["revenue_contribution_%"] = (
    df.groupby("cluster")["total_revenue"].sum()
    / df["total_revenue"].sum()
).values * 100

print("\nCluster Performance Summary:")
print(cluster_summary)

overlap = pd.crosstab(
    df["strategic_segment"],
    df["cluster"],
    margins=True
)

print("\nOverlap Table (Strategic vs Cluster):")
print(overlap)

export_cols = [
    "customer_id",
    "total_revenue",
    "order_count",
    "avg_order_value",
    "avg_discount_lifetime",
    "revenue_first_30_days",
    "orders_first_30_days",
    "strategic_segment",
    "cluster"
]

export_df = df[export_cols]

export_df.to_csv(
    r"C:\Users\Vedika\OneDrive\Desktop\shopsphere-project\data\model5_segmentation.csv",
    index=False
)

print("\nCSV exported successfully.")
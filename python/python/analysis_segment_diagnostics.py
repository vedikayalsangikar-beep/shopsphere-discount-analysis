import pandas as pd
import sqlite3

conn = sqlite3.connect(r"C:\Users\Vedika\OneDrive\Desktop\shopsphere-project\data\shopsphere.db")

df = pd.read_sql("SELECT * FROM model6_segment_diagnostics", conn)

total_customers = df["customers"].sum()
total_revenue = df["total_revenue"].sum()
overall_avg_revenue = total_revenue / total_customers

df["customer_share_%"] = df["customers"] / total_customers * 100
df["revenue_contribution_%"] = df["total_revenue"] / total_revenue * 100
df["efficiency_index"] = df["avg_revenue_per_customer"] / overall_avg_revenue

df = df.sort_values(by="revenue_contribution_%", ascending=False)
df["cumulative_revenue_%"] = df["revenue_contribution_%"].cumsum()

print("\nModel 6 – Segment Economic Diagnostics\n")
print(df)

# Export for Tableau
df.to_csv(
    r"C:\Users\Vedika\OneDrive\Desktop\shopsphere-project\data\analysis_segment_diagnostics.csv",
    index=False
)

print("\nCSV exported successfully.")

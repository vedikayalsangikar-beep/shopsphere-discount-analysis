import pandas as pd
import sqlite3
import numpy as np

conn = sqlite3.connect("data/shopsphere.db")

# Load early behavior
early = pd.read_sql("SELECT * FROM customer_early_behavior", conn)

# Load lifetime summary
lifetime = pd.read_sql("""
    SELECT 
        customer_id,
        total_revenue,
        age,
        gender,
        income_band,
        discount_bucket
    FROM customer_summary
""", conn)

# Merge
df = early.merge(lifetime, on="customer_id")

print(df.head())
print(df.shape)
cutoff = df["total_revenue"].quantile(0.75)

df["high_value_customer"] = (df["total_revenue"] >= cutoff).astype(int)

print("High-value cutoff:", cutoff)
print(df["high_value_customer"].value_counts())

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Select predictors
features = [
    "orders_first_30_days",
    "revenue_first_30_days",
    "avg_discount_first_30_days"
]

X = df[features]
y = df["high_value_customer"]

# Fill potential NaNs from avg()
X = X.fillna(0)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train logistic regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# Custom threshold
threshold = 0.30

y_pred_custom = (y_prob >= threshold).astype(int)

print(classification_report(y_test, y_pred_custom))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# One-hot encode categorical variables
df = pd.get_dummies(
    df,
    columns=["gender", "income_band", "discount_bucket"],
    drop_first=True
)

features = [
    "orders_first_30_days",
    "revenue_first_30_days",
    "avg_discount_first_30_days",
    "age"
] + [col for col in df.columns if 
     col.startswith("gender_") or
     col.startswith("income_band_") or
     col.startswith("discount_bucket_")]

x= df[features].fillna(0)
y= df["high_value_customer"]

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# Prevent division by zero
df["orders_first_30_days"] = df["orders_first_30_days"].replace(0, np.nan)

df["avg_order_value_first_30"] = (
    df["revenue_first_30_days"] /
    df["orders_first_30_days"]
)

df["orders_first_30_days"] = df["orders_first_30_days"].fillna(0)
df["avg_order_value_first_30"] = df["avg_order_value_first_30"].fillna(0)

# Early revenue median indicator
early_cutoff = df["revenue_first_30_days"].median()
df["high_early_revenue_flag"] = (
    df["revenue_first_30_days"] >= early_cutoff
).astype(int)

# Get feature names safely
feature_names = X.columns

coefficients = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": model.coef_[0]
})

coefficients = coefficients.sort_values(by="Coefficient", ascending=False)

print(coefficients)

# Create quartiles of early revenue
df["early_revenue_quartile"] = pd.qcut(
    df["revenue_first_30_days"],
    4,
    labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"]
)

# Aggregate lifetime revenue by quartile
quartile_summary = df.groupby("early_revenue_quartile")["total_revenue"].mean().reset_index()

print(quartile_summary)

# Export for Tableau
quartile_summary.to_csv("data/model3_early_vs_lifetime.csv", index=False)

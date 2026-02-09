Do Discounts Really Drive Revenue?

An end-to-end e-commerce analytics project

📌 Project Overview
This project analyzes the impact of discounting on order-level revenue for a simulated e-commerce platform.
Using SQL, Python, and Tableau, the analysis evaluates whether discounts meaningfully increase revenue or whether they erode value despite higher order volumes.

📊 Dataset
Synthetic but behaviorally realistic transactional data:

• 505 customers

• 60 products

• 3,000 order

🧠 Analytical Approach

• Designed a relational database schema in SQLite

• Generated customer, product, and order data using Python

• Performed SQL joins and aggregations for exploratory analysis

• Modelled order-level revenue using OLS regression

• Validated findings visually using Tableau

⭐ Key Insight

Discounts have a statistically significant negative impact on order revenue, and the revenue loss is not compensated by increased order volumes.

📈 Evidence

• Regression analysis (R² ≈ 0.89) shows strong negative discount coefficients

• Visual analysis confirms declining average order value and revenue as discounts increase

🧰 Tools Used

• SQL (SQLite)

• Python (pandas, statsmodels, matplotlib)

• Tableau Public

📁 Repository Structure

• /data → SQLite database & Tableau-ready CSV

• /python → data generation and regression analysis scripts

• /tableau → dashboard screenshot

• case-study.pdf → one-page project summary

🔗 Tableau Dashboard

https://public.tableau.com/views/DoDiscountsReallyDriveRevenue/DoDiscountsReallyDriveRevenue?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

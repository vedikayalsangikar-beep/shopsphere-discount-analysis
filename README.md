**Shopsphere — End-to-End E-Commerce Analytics Case Study**

An applied analytics project exploring revenue performance, retention dynamics, early customer signals, and segmentation strategy in a simulated e-commerce environment.

This repository demonstrates SQL-based data modelling, statistical analysis in Python, and business-oriented visualization in Tableau.


**Tools & Technologies**

• SQL (SQLite) — relational schema design, joins, aggregations, feature engineering

• Python — pandas, statsmodels, scikit-learn

• Statistical Methods — OLS regression, logistic regression, hypothesis testing

• Machine Learning — K-Means clustering (unsupervised segmentation)

• Data Visualization — Tableau Public dashboards

• Business Communication — Executive-ready 1–2 page case studies


**Dataset**

Synthetic but behaviorally realistic transactional dataset:

• 505 customers

• 3,000+ orders

• Multi-category products

• Engineered customer-level features

All data generation scripts are included and reproducible.

**Model Breakdown**

**Model 1 — Discount Impact on Revenue**

Question: Do discounts meaningfully increase order-level revenue?

Method: OLS regression on order-level revenue

Outcome: Discounts showed a statistically significant negative relationship with revenue; price and quantity were stronger drivers.

**Model 2 — Discounts & Customer Retention**

Question: Do discounted customers exhibit higher repeat rates?

Method: Customer-level retention analysis

Outcome: Higher discounts did not consistently improve repeat behavior; volume increases did not offset margin effects.

**Model 3 — Early Signals of High-Value Customers**

Question: Can early behavior predict long-term customer value?

Method: Logistic regression using first 30-day behavioral features

Outcome: Early revenue and order frequency showed meaningful predictive power for identifying high-value customers.

**Model 4 — Statistical Early Behavioral Lift**

Question: Which early behaviors significantly differentiate high-value customers?

Method: Mean comparison, lift %, hypothesis testing

Outcome: Revenue generated in the first 30 days showed strong statistical lift; discount depth did not.

**Model 5 — Strategic vs Data-Driven Segmentation**

Question: How does rule-based segmentation compare to clustering?

Method: Strategic segmentation + K-Means clustering

Outcome: Clustering revealed behavioral structure not fully captured by rule-based segments, 
highlighting trade-offs between interpretability and discovery.


**Repository Structure**

• data/              → SQLite database & derived datasets  

• python/            → Data generation & analysis scripts  

• visuals/           → Python-generated charts  

• tableau/           → Dashboard exports  

• case-studies/      → One-page executive PDFs per model  

• README.md

**Skills Demonstrated**

• Structured analytical problem framing

• Statistical modelling & inference

• Customer-level feature engineering

• Predictive signal identification

• Segmentation strategy comparison

• Business-facing communication of quantitative findings

**Dashboards & Case Studies**

• Each model includes:

• Tableau dashboard

• One-page executive summary (PDF)

• Reproducible Python code
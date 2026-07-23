# data-analytics-ecommerce
# Data Analytics Project: E-Commerce Sales & Customer Insights
An end-to-end Python data analytics project that cleans, interrogates, and visualizes sales, product performance, customer behavior, and order distributions from an e-commerce dataset.
# 📌 Project Overview:
This repository contains a full data analytics pipeline designed to process and analyze order transactions (Cleaned_Dataset_for_Data_Analytics.csv). The project computes key descriptive statistics, detects high-value transaction outliers using the IQR method, evaluates promotion/coupon performance, and generates publication-ready visualizations.
# Key Objectives:
Descriptive Statistics: Calculate key baseline metrics (Mean, Median, Standard Deviation, IQR, Count).Outlier & Distribution Analysis: Interrogate right-skewed pricing and separate actual business signals from noise.Product & Promotional Tracking: Measure revenue contribution by product category and coupon effectiveness.Automated Visualizations: Export analytical charts for monthly revenue trends, order distributions, and coupon impacts.
# 📊 Summary of InsightsRevenue Baseline:
Total revenue reached $1,264,761.96 across 1,200 orders.Distribution & Outliers: Total Price is right-skewed ($\text{Mean} = \$1,053.97$ vs. $\text{Median} = \$823.62$). 8 statistical outliers ($> \$3,332.41$) were identified using the IQR method—all determined to be legitimate bulk orders (5 units at premium prices) rather than data errors.Product Performance: Top revenue drivers are Chairs ($195.6k), Printers ($195.6k), and Laptops ($192.1k).Fulfillment Bottleneck: Cancellations and returns account for ~41.4% of total orders, highlighting a primary area for operational optimization.
# 🛠️ Tech Stack & Dependencies
Language: Python 3.8+
Data Processing: pandas, numpy
Visualization: matplotlib, seaborn
# Author 
SHUJAH ALI SHAUKET

# 📁 Repository Structure;
├── Cleaned_Dataset_for_Data_Analytics.csv    # Source CSV dataset
├── data_analytics_pipeline.py                 # Main Python execution script
├── README.md                                  # Project documentation
└── generated_charts/                          # Output visual figures
   ├── distribution_outliers_analysis.png
   ├── monthly_revenue_trend.png
   └── coupon_and_status_summary.png

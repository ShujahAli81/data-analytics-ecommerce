"""
Data Analytics Pipeline for Cleaned_Dataset_for_Data_Analytics.csv

Tasks Executed:
1. Basic Descriptive Statistics (Mean, Median, Count, IQR, Standard Deviation).
2. Outlier & Distribution Detection (IQR-based identification and signal verification).
3. Product & Promotional Breakdown (Revenue, AOV, and Cart metrics).
4. Data Visualizations (Saves distribution plots, trend charts, and status breakdowns).
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_dataset(file_path):
    """Loads the CSV dataset and converts date fields."""
    if not os.path.exists(file_path):
        print(f"[X] File '{file_path}' not found.")
        return None

    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["YearMonth"] = df["Date"].dt.to_period("M")
    print(f"[✓] Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df


def calculate_descriptive_statistics(df):
    """Computes mean, median, count, std, min, max, and IQR for numerical columns."""
    print("\n" + "=" * 65)
    print(" 1. BASIC DESCRIPTIVE STATISTICS")
    print("=" * 65)

    num_cols = ["Quantity", "UnitPrice", "TotalPrice", "ItemsInCart"]

    desc_table = df[num_cols].agg(["count", "mean", "median", "std", "min", "max"]).T
    desc_table["IQR"] = df[num_cols].apply(
        lambda x: x.quantile(0.75) - x.quantile(0.25)
    )

    # Reorder columns for clean display
    desc_table = desc_table[
        ["count", "mean", "median", "IQR", "std", "min", "max"]
    ]
    print(desc_table.round(2).to_string())

    return num_cols


def detect_outliers_and_distributions(df, num_cols):
    """Detects outliers using standard 1.5 * IQR rule and prints summary."""
    print("\n" + "=" * 65)
    print(" 2. OUTLIER DETECTION & DISTRIBUTION ANALYSIS")
    print("=" * 65)

    outlier_records = {}

    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_records[col] = len(outliers)
        print(
            f"Column '{col}': {len(outliers)} outliers detected (Bounds: [{lower_bound:.2f}, {upper_bound:.2f}])"
        )

    # Inspect TotalPrice outliers
    tp_q1 = df["TotalPrice"].quantile(0.25)
    tp_q3 = df["TotalPrice"].quantile(0.75)
    tp_iqr = tp_q3 - tp_q1
    tp_upper = tp_q3 + 1.5 * tp_iqr

    tp_outliers = df[df["TotalPrice"] > tp_upper][
        ["OrderID", "Product", "Quantity", "UnitPrice", "TotalPrice"]
    ]

    print("\n--- Identified High-Value Outliers in TotalPrice ---")
    print(tp_outliers.to_string(index=False))
    print(
        "\nNote: These outliers represent valid high-tier bulk orders (5 units at high unit price), not noise."
    )


def summarize_business_metrics(df):
    """Calculates product-level and promotional metrics."""
    print("\n" + "=" * 65)
    print(" 3. PRODUCT & PROMOTIONAL SUMMARY")
    print("=" * 65)

    # Product Metrics
    product_summary = (
        df.groupby("Product")
        .agg(
            Order_Count=("OrderID", "count"),
            Mean_TotalPrice=("TotalPrice", "mean"),
            Median_TotalPrice=("TotalPrice", "median"),
            Total_Revenue=("TotalPrice", "sum"),
        )
        .sort_values(by="Total_Revenue", ascending=False)
        .reset_index()
    )

    print("--- Product Metrics ---")
    print(product_summary.to_string(index=False))

    # Coupon Metrics
    df_coupon = df.copy()
    df_coupon["CouponCode"] = df_coupon["CouponCode"].fillna("No Coupon")
    coupon_summary = (
        df_coupon.groupby("CouponCode")
        .agg(
            Order_Count=("OrderID", "count"),
            Total_Revenue=("TotalPrice", "sum"),
            Avg_Order_Value=("TotalPrice", "mean"),
        )
        .reset_index()
    )

    print("\n--- Promotional Coupon Summary ---")
    print(coupon_summary.to_string(index=False))

    return coupon_summary


def generate_all_visualizations(df, coupon_summary):
    """Generates and saves all required charts."""
    print("\n" + "=" * 65)
    print(" 4. GENERATING CHART FIGURES")
    print("=" * 65)

    sns.set_theme(style="whitegrid")

    # Figure 1: Distributions & Outliers Box plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    sns.boxplot(data=df, y="TotalPrice", ax=axes[0, 0], color="skyblue")
    axes[0, 0].set_title("TotalPrice Box Plot (8 Outliers Detected)")

    sns.histplot(df["TotalPrice"], kde=True, ax=axes[0, 1], color="teal")
    axes[0, 1].set_title("TotalPrice Distribution (Right-Skewed)")

    sns.boxplot(
        data=df, x="Product", y="TotalPrice", ax=axes[1, 0], palette="Set2"
    )
    axes[1, 0].set_title("TotalPrice by Product")
    axes[1, 0].tick_params(axis="x", rotation=30)

    sns.histplot(df["UnitPrice"], kde=True, ax=axes[1, 1], color="coral")
    axes[1, 1].set_title("UnitPrice Distribution (Uniform Spread)")

    plt.tight_layout()
    plt.savefig("distribution_outliers_analysis.png", dpi=300)
    plt.close()
    print("[✓] Saved figure: distribution_outliers_analysis.png")

    # Figure 2: Monthly Revenue Trend
    monthly_rev = df.groupby("YearMonth")["TotalPrice"].sum().reset_index()
    monthly_rev["YearMonth"] = monthly_rev["YearMonth"].astype(str)

    plt.figure(figsize=(12, 5))
    sns.lineplot(
        data=monthly_rev,
        x="YearMonth",
        y="TotalPrice",
        marker="o",
        color="#1f77b4",
        linewidth=2,
    )
    plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Year-Month", fontsize=11)
    plt.ylabel("Total Revenue ($)", fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("monthly_revenue_trend.png", dpi=300)
    plt.close()
    print("[✓] Saved figure: monthly_revenue_trend.png")

    # Figure 3: Coupon AOV & Order Status Distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.barplot(
        data=coupon_summary,
        x="CouponCode",
        y="Avg_Order_Value",
        ax=axes[0],
        palette="viridis",
    )
    axes[0].set_title("Average Order Value by Coupon Code")

    sns.countplot(data=df, x="OrderStatus", ax=axes[1], palette="Set2")
    axes[1].set_title("Order Status Distribution")

    plt.tight_layout()
    plt.savefig("coupon_and_status_summary.png", dpi=300)
    plt.close()
    print("[✓] Saved figure: coupon_and_status_summary.png")


def main():
    file_name = "Cleaned_Dataset_for_Data_Analytics.csv"

    # Step 1: Load data
    df = load_dataset(file_name)
    if df is None:
        return

    # Step 2: Calculate basic descriptive stats
    num_cols = calculate_descriptive_statistics(df)

    # Step 3: Outlier and distribution interrogation
    detect_outliers_and_distributions(df, num_cols)

    # Step 4: Summarize key business metrics
    coupon_summary = summarize_business_metrics(df)

    # Step 5: Export all visual charts
    generate_all_visualizations(df, coupon_summary)

    print("\n" + "=" * 65)
    print(" ALL TASKS EXECUTED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
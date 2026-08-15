"""Inflation and consumer basket composition.

Libraries used: pandas, NumPy, Matplotlib, Seaborn.
Run: python analysis.py
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib_cache"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DATA_FILE = BASE_DIR / "data" / "consumer_basket_2020_2023.csv"
FIGURES_DIR = BASE_DIR / "figures"
THRESHOLD = 4.5
NECESSITIES = ["food_at_home", "housing", "transportation", "healthcare"]
LUXURIES = ["food_away_from_home", "alcoholic_beverages", "apparel_and_services", "entertainment", "personal_care", "reading"]


def prepare_data():
    df = pd.read_csv(DATA_FILE)
    df["necessity_spending"] = np.sum(df[NECESSITIES].to_numpy(), axis=1)
    df["luxury_spending"] = np.sum(df[LUXURIES].to_numpy(), axis=1)
    df["necessity_share_pct"] = np.divide(100 * df["necessity_spending"], df["total_expenditure"])
    df["luxury_share_pct"] = np.divide(100 * df["luxury_spending"], df["total_expenditure"])
    df["luxury_to_necessity_ratio"] = np.divide(df["luxury_spending"], df["necessity_spending"])
    df["inflation_group"] = np.where(df["inflation_pct"] >= THRESHOLD, f"High (>={THRESHOLD}%)", f"Lower (<{THRESHOLD}%)")
    return df


def make_charts(df):
    FIGURES_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="colorblind")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df, x="year", y="inflation_pct", hue="inflation_group", dodge=False, ax=ax)
    ax.axhline(THRESHOLD, color="black", linestyle="--", label=f"Threshold = {THRESHOLD}%")
    ax.set(title="Annual U.S. CPI-U Inflation", xlabel="Year", ylabel="Inflation (%)")
    ax.legend(title="Inflation group")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "01_inflation_threshold.png", dpi=200)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=df, x="year", y="necessity_share_pct", marker="o", linewidth=2.5, label="Necessity share", ax=ax)
    sns.lineplot(data=df, x="year", y="luxury_share_pct", marker="o", linewidth=2.5, label="Luxury share", ax=ax)
    ax.set(title="Defined Basket Shares of Total Household Spending", xlabel="Year", ylabel="Share of total expenditure (%)")
    ax.set_xticks(df["year"])
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "02_basket_shares_over_time.png", dpi=200)

    means = df.groupby("inflation_group", observed=True)[["necessity_share_pct", "luxury_share_pct"]].mean().reset_index()
    chart_data = means.melt(id_vars="inflation_group", var_name="basket", value_name="average_share_pct")
    chart_data["basket"] = chart_data["basket"].map({"necessity_share_pct": "Necessities", "luxury_share_pct": "Luxuries"})
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=chart_data, x="inflation_group", y="average_share_pct", hue="basket", ax=ax)
    ax.set(title="Average Basket Share Below vs. At/Above the Threshold", xlabel="Inflation group", ylabel="Average share (%)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "03_threshold_comparison.png", dpi=200)


def main():
    df = prepare_data()
    df.round(3).to_csv(BASE_DIR / "results_summary.csv", index=False)

    print("\n--- Complete CSV Data with Calculations ---")
    print(df.round(3).to_string(index=False))

    make_charts(df)
    averages = df.groupby("inflation_group", observed=True)["luxury_to_necessity_ratio"].mean()
    print("\n--- Average Luxury-to-Necessity Ratio ---")
    print(averages.round(3))
    print("\nCharts and results_summary.csv created successfully.")
    plt.show()


if __name__ == "__main__":
    main()

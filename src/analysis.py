"""Inflation and Consumer Basket Composition Analysis (IEEE Enhanced Pipeline).

Libraries used: pandas, NumPy, SciPy, Matplotlib, Seaborn.
Run: python analysis.py
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib_cache"))

DATA_FILE = BASE_DIR / "data" / "consumer_basket_2020_2023.csv"
FIGURES_DIR = BASE_DIR / "figures"
THRESHOLD = 4.5

NECESSITIES = ["food_at_home", "housing", "transportation", "healthcare"]
LUXURIES = [
    "food_away_from_home",
    "alcoholic_beverages",
    "apparel_and_services",
    "entertainment",
    "personal_care",
    "reading",
]


def prepare_data() -> pd.DataFrame:
    """Loads raw expenditure data and calculates basket metrics,

    deflated real spending proxies, and YoY growth rates.
    """
    df = pd.read_csv(DATA_FILE)

    df["necessity_spending"] = df[NECESSITIES].sum(axis=1)
    df["luxury_spending"] = df[LUXURIES].sum(axis=1)

    df["necessity_share_pct"] = (
        df["necessity_spending"] / df["total_expenditure"]
    ) * 100
    df["luxury_share_pct"] = (
        df["luxury_spending"] / df["total_expenditure"]
    ) * 100
    df["luxury_to_necessity_ratio"] = (
        df["luxury_spending"] / df["necessity_spending"]
    )

    df["inflation_group"] = np.where(
        df["inflation_pct"] >= THRESHOLD,
        f"High (>={THRESHOLD}%)",
        f"Lower (<{THRESHOLD}%)",
    )

    # YoY Growth Metrics
    df["necessity_growth_pct"] = df["necessity_spending"].pct_change() * 100
    df["luxury_growth_pct"] = df["luxury_spending"].pct_change() * 100

    return df


def calculate_statistics(df: pd.DataFrame) -> dict:
    high_inf = df[df["inflation_pct"] >= THRESHOLD][
        "luxury_to_necessity_ratio"
    ]
    low_inf = df[df["inflation_pct"] < THRESHOLD]["luxury_to_necessity_ratio"]

    # Two-sample t-test (equal_var=False for Welch's t-test)
    t_stat, p_val = stats.ttest_ind(high_inf, low_inf, equal_var=False)

    regime_summary = (
        df.groupby("inflation_group", observed=True)
        .agg(
            mean_ratio=("luxury_to_necessity_ratio", "mean"),
            std_ratio=("luxury_to_necessity_ratio", "std"),
            mean_nec_share=("necessity_share_pct", "mean"),
            mean_lux_share=("luxury_share_pct", "mean"),
        )
        .reset_index()
    )

    return {
        "regime_summary": regime_summary,
        "t_statistic": t_stat,
        "p_value": p_val,
    }


def make_charts(df: pd.DataFrame):
    FIGURES_DIR.mkdir(exist_ok=True)
    sns.set_theme(
        style="whitegrid",
        palette="colorblind",
        font="sans-serif",
        font_scale=1.1,
    )

    # Figure 1: Inflation Threshold Barplot
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    sns.barplot(
        data=df,
        x="year",
        y="inflation_pct",
        hue="inflation_group",
        dodge=False,
        ax=ax1,
    )
    ax1.axhline(
        THRESHOLD,
        color="crimson",
        linestyle="--",
        linewidth=1.8,
        label=f"Threshold ($\\tau = {THRESHOLD}\\%$)",
    )
    ax1.set(
        title="Annual U.S. CPI-U Inflation (2020–2023)",
        xlabel="Year",
        ylabel="CPI-U Inflation Rate (%)",
    )
    ax1.legend(title="Macroeconomic Regime", loc="upper right")
    fig1.tight_layout()
    fig1.savefig(
        FIGURES_DIR / "01_inflation_threshold.png", dpi=300, bbox_inches="tight"
    )

    # Figure 2: Longitudinal Basket Shares
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(
        data=df,
        x="year",
        y="necessity_share_pct",
        marker="o",
        linewidth=2.5,
        label="Necessities Share (%)",
        ax=ax2,
    )
    sns.lineplot(
        data=df,
        x="year",
        y="luxury_share_pct",
        marker="s",
        linewidth=2.5,
        label="Discretionary / Luxury Share (%)",
        ax=ax2,
    )
    ax2.set(
        title="Expenditure Basket Share Dynamics Over Time",
        xlabel="Year",
        ylabel="Share of Total Household Budget (%)",
    )
    ax2.set_xticks(df["year"])
    ax2.legend(loc="center right")
    fig2.tight_layout()
    fig2.savefig(
        FIGURES_DIR / "02_basket_shares_over_time.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Figure 3: Multi-Panel Regime Comparison
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))

    # Subplot A: Basket Shares
    means = (
        df.groupby("inflation_group", observed=True)[
            ["necessity_share_pct", "luxury_share_pct"]
        ]
        .mean()
        .reset_index()
    )
    chart_data = means.melt(
        id_vars="inflation_group",
        var_name="basket",
        value_name="average_share_pct",
    )
    chart_data["basket"] = chart_data["basket"].map(
        {
            "necessity_share_pct": "Necessities",
            "luxury_share_pct": "Discretionary",
        }
    )

    sns.barplot(
        data=chart_data,
        x="inflation_group",
        y="average_share_pct",
        hue="basket",
        ax=ax3a,
    )
    ax3a.set(
        title="(A) Basket Budget Allocation",
        xlabel="Inflation Regime",
        ylabel="Average Share (%)",
    )

    # Subplot B: Luxury-to-Necessity Ratio (R_LN)
    sns.barplot(
        data=df,
        x="inflation_group",
        y="luxury_to_necessity_ratio",
        hue="inflation_group",
        legend=False,
        estimator=np.mean,
        errorbar=None,
        ax=ax3b,
        #palette="crest",
    )
    ax3b.set(
        title="(B) Mean Luxury-to-Necessity Ratio ($R_{LN}$)",
        xlabel="Inflation Regime",
        ylabel="Ratio ($S_{lux} / S_{nec}$)",
    )

    fig3.suptitle("Comparative Analysis Across Inflation Regimes", fontsize=14)
    fig3.tight_layout()
    fig3.savefig(
        FIGURES_DIR / "03_threshold_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )


def main():
    df = prepare_data()
    stats_dict = calculate_statistics(df)

    # Export Processed Dataset
    output_path = BASE_DIR / "results_summary.csv"
    df.round(4).to_csv(output_path, index=False)

    print("\n" + "=" * 55)
    print("      INFLATIONARY BASKET COMPOSITION RESULTS")
    print("=" * 55)
    print(df.round(3).to_string(index=False))

    print("\n" + "-" * 55)
    print("             REGIME SUMMARY STATISTICS")
    print("-" * 55)
    print(stats_dict["regime_summary"].round(4).to_string(index=False))

    print("\n" + "-" * 55)
    print("             HYPOTHESIS TESTING (WELCH'S T-TEST)")
    print("-" * 55)
    print(f"t-statistic : {stats_dict['t_statistic']:.4f}")
    print(f"p-value     : {stats_dict['p_value']:.4f}")
    print(
        f"Inference   : Difference is "
        f"{'statistically significant (p < 0.05)' if stats_dict['p_value'] < 0.05 else 'not statistically significant (p >= 0.05)'}"
    )

    make_charts(df)
    print("\nVisualizations and results_summary.csv exported successfully.")
    plt.show()


if __name__ == "__main__":
    main()

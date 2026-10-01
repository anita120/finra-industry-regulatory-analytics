import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# FINRA Industry Regulatory Analytics
# Python Visualization / EDA
# ============================================================

# Project paths
PROJECT_ROOT = Path(r"F:\finra_industry_regulatory_analytics")

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "finra_industry_snapshot_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "visualizations"
)

# Create output directory if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. Load cleaned data
# ============================================================

df = pd.read_csv(INPUT_FILE)

# Convert report date to datetime
df["reportDate"] = pd.to_datetime(df["reportDate"])

print("=" * 60)
print("FINRA DATASET")
print("=" * 60)

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Years:", df["year"].min(), "-", df["year"].max())
print(
    "Categories:",
    df["registrationTypeAtEndOfYear"].nunique()
)
print()


# ============================================================
# 2. Select the clean 2011-2021 analytical snapshot
# ============================================================
#
# The FINRA API contains overlapping report dates.
#
# We use:
#   2021-12-31 for 2011 and 2021
#   2022-12-31 for 2012-2020
#
# This matches the SQL analysis.


selected_2022 = df[
    (df["reportDate"] == "2022-12-31")
    & (df["year"].between(2012, 2020))
]

selected_2021 = df[
    (df["reportDate"] == "2021-12-31")
    & (df["year"].isin([2011, 2021]))
]


analysis_df = pd.concat(
    [selected_2022, selected_2021],
    ignore_index=True
)

analysis_df = analysis_df.sort_values(
    ["year", "registrationTypeAtEndOfYear"]
)


print("ANALYTICAL DATASET")
print("-" * 60)
print("Rows:", len(analysis_df))
print(
    "Years:",
    analysis_df["year"].min(),
    "-",
    analysis_df["year"].max()
)
print()


# ============================================================
# 3. Create wide-format trend dataset
# ============================================================

trend_df = analysis_df.pivot(
    index="year",
    columns="registrationTypeAtEndOfYear",
    values="numberOfFirms"
)

trend_df = trend_df.sort_index()


# ============================================================
# 4. Visualization 1
# All FINRA-Registered Broker-Dealer Firms
# ============================================================

category = (
    "All FINRA-Registered Broker-Dealer Firms at Year End"
)

plt.figure(figsize=(10, 6))

plt.plot(
    trend_df.index,
    trend_df[category],
    marker="o"
)

plt.title(
    "FINRA-Registered Broker-Dealer Firms, 2011-2021"
)

plt.xlabel("Year")
plt.ylabel("Number of Firms")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "01_broker_dealer_trend.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 5. Visualization 2
# Investment Adviser Firms-Only
# ============================================================

category = (
    "Investment Adviser Firms-Only at Year End"
)

plt.figure(figsize=(10, 6))

plt.plot(
    trend_df.index,
    trend_df[category],
    marker="o"
)

plt.title(
    "Investment Adviser Firms-Only, 2011-2021"
)

plt.xlabel("Year")
plt.ylabel("Number of Firms")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "02_investment_adviser_trend.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 6. Visualization 3
# All Registration Categories
# ============================================================

plt.figure(figsize=(12, 7))

for column in trend_df.columns:

    plt.plot(
        trend_df.index,
        trend_df[column],
        marker="o",
        label=column
    )


plt.title(
    "FINRA Registration Category Trends, 2011-2021"
)

plt.xlabel("Year")
plt.ylabel("Reported Firm Count")

plt.legend(
    fontsize=8,
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "03_registration_category_trends.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 7. Visualization 4
# 2011 vs 2021 Comparison
# ============================================================

comparison_df = trend_df.loc[
    [2011, 2021]
].T

comparison_df.columns = [
    "2011",
    "2021"
]

comparison_df["Change"] = (
    comparison_df["2021"]
    - comparison_df["2011"]
)

comparison_df = comparison_df.sort_values(
    "Change"
)


plt.figure(figsize=(12, 7))

x = range(len(comparison_df))

plt.barh(
    list(x),
    comparison_df["Change"]
)

plt.yticks(
    list(x),
    comparison_df.index,
    fontsize=8
)

plt.axvline(
    0,
    linewidth=1
)

plt.title(
    "Change in Reported Registration Categories, 2011-2021"
)

plt.xlabel(
    "Change in Number of Reported Firms"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "04_category_change_2011_2021.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 8. Visualization 5
# Broker-Dealer vs Investment Adviser
# ============================================================

broker_category = (
    "All FINRA-Registered Broker-Dealer Firms at Year End"
)

adviser_category = (
    "Investment Adviser Firms-Only at Year End"
)


plt.figure(figsize=(10, 6))

plt.plot(
    trend_df.index,
    trend_df[broker_category],
    marker="o",
    label="Broker-Dealer Firms"
)

plt.plot(
    trend_df.index,
    trend_df[adviser_category],
    marker="o",
    label="Investment Adviser Firms-Only"
)

plt.title(
    "Broker-Dealer vs Investment Adviser Firm Trends"
)

plt.xlabel("Year")
plt.ylabel("Number of Firms")

plt.legend()

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "05_broker_vs_adviser.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 9. Visualization 6
# Year-over-Year Percentage Change
# ============================================================

yoy_df = trend_df.pct_change() * 100


plt.figure(figsize=(12, 7))

for column in yoy_df.columns:

    plt.plot(
        yoy_df.index,
        yoy_df[column],
        marker="o",
        label=column
    )


plt.axhline(
    0,
    linewidth=1
)

plt.title(
    "Year-over-Year Change by Registration Category"
)

plt.xlabel("Year")
plt.ylabel("YoY Change (%)")

plt.legend(
    fontsize=8,
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        str(OUTPUT_DIR),
        "06_yoy_percentage_change.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 10. Export analytical datasets
# ============================================================

analysis_df.to_csv(
    os.path.join(
        str(OUTPUT_DIR),
        "finra_analysis_dataset.csv"
    ),
    index=False
)

trend_df.to_csv(
    os.path.join(
        str(OUTPUT_DIR),
        "finra_trend_dataset.csv"
    )
)


# ============================================================
# 11. Final status
# ============================================================

print()
print("=" * 60)
print("VISUALIZATION COMPLETE")
print("=" * 60)

print("Output folder:")
print(str(OUTPUT_DIR))

print()
print("Files created:")

for file_name in sorted(os.listdir(str(OUTPUT_DIR))):

    print(" -", file_name)

print()
print("FINRA Python EDA completed successfully.")
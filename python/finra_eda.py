import os
import pandas as pd
import numpy as np


# ============================================================
# FINRA Industry Regulatory Analytics
# Exploratory Data Analysis (EDA)
# ============================================================

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

BASE_DIR = r"F:\finra_industry_regulatory_analytics"

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "finra_industry_snapshot_clean.csv"
)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("=" * 70)
print("FINRA INDUSTRY REGULATORY ANALYTICS - EDA")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ------------------------------------------------------------
# 3. Display basic information
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("1. DATASET INFORMATION")
print("-" * 70)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head())


# ------------------------------------------------------------
# 4. Missing values
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("2. MISSING VALUE CHECK")
print("-" * 70)

missing_values = df.isnull().sum()

print(missing_values)

if missing_values.sum() == 0:
    print("\nNo missing values found.")
else:
    print("\nMissing values detected.")


# ------------------------------------------------------------
# 5. Duplicate check
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("3. DUPLICATE CHECK")
print("-" * 70)

duplicate_rows = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_rows}")

if duplicate_rows == 0:
    print("No duplicate rows found.")
else:
    print("Duplicate rows detected.")


# ------------------------------------------------------------
# 6. Convert data types
# ------------------------------------------------------------

df["year"] = pd.to_numeric(df["year"], errors="coerce")

df["number_of_firms"] = pd.to_numeric(
    df["number_of_firms"],
    errors="coerce"
)

df["reportDate"] = pd.to_datetime(
    df["reportDate"],
    errors="coerce"
)


# ------------------------------------------------------------
# 7. Year analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("4. YEAR ANALYSIS")
print("-" * 70)

print(f"Minimum year: {df['year'].min()}")
print(f"Maximum year: {df['year'].max()}")
print(f"Number of years: {df['year'].nunique()}")

print("\nYears covered:")
print(sorted(df["year"].dropna().unique()))


# ------------------------------------------------------------
# 8. Report date analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("5. REPORT DATE ANALYSIS")
print("-" * 70)

print(f"Number of report dates: {df['reportDate'].nunique()}")

print("\nReport dates:")
print(
    sorted(
        df["reportDate"]
        .dropna()
        .dt.strftime("%Y-%m-%d")
        .unique()
    )
)


# ------------------------------------------------------------
# 9. Registration category analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("6. REGISTRATION CATEGORY ANALYSIS")
print("-" * 70)

categories = df["registrationTypeAtEndOfYear"].dropna().unique()

print(f"Number of registration categories: {len(categories)}")

print("\nRegistration categories:")

for category in sorted(categories):
    print(f"- {category}")


# ------------------------------------------------------------
# 10. Category record counts
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("7. RECORDS BY REGISTRATION CATEGORY")
print("-" * 70)

category_counts = (
    df["registrationTypeAtEndOfYear"]
    .value_counts()
    .sort_index()
)

print(category_counts)


# ------------------------------------------------------------
# 11. Individual/Firm analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("8. INDIVIDUAL / FIRM ANALYSIS")
print("-" * 70)

print(
    df["individualOrFirm"]
    .value_counts()
)


# ------------------------------------------------------------
# 12. Number of firms summary statistics
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("9. NUMBER OF FIRMS SUMMARY")
print("-" * 70)

print(
    df["number_of_firms"]
    .describe()
)


# ------------------------------------------------------------
# 13. Minimum / Maximum firm counts
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("10. FIRM COUNT RANGE")
print("-" * 70)

print(
    f"Minimum number of firms: "
    f"{df['number_of_firms'].min():,.0f}"
)

print(
    f"Maximum number of firms: "
    f"{df['number_of_firms'].max():,.0f}"
)

print(
    f"Average number of firms: "
    f"{df['number_of_firms'].mean():,.2f}"
)

print(
    f"Total reported observations: "
    f"{df['number_of_firms'].sum():,.0f}"
)


# ------------------------------------------------------------
# 14. Analyze duplicate historical snapshots
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("11. YEAR / REPORT DATE DISTRIBUTION")
print("-" * 70)

year_report_summary = (
    df.groupby(["year", "reportDate"])
    .size()
    .reset_index(name="records")
)

print(year_report_summary.to_string(index=False))


# ------------------------------------------------------------
# 15. Identify duplicate year/category combinations
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("12. YEAR / CATEGORY DUPLICATE ANALYSIS")
print("-" * 70)

year_category_counts = (
    df.groupby(
        ["year", "registrationTypeAtEndOfYear"]
    )
    .size()
    .reset_index(name="records")
)

duplicate_business_keys = year_category_counts[
    year_category_counts["records"] > 1
]

if duplicate_business_keys.empty:
    print(
        "No duplicate year/category combinations found."
    )
else:
    print(
        "Multiple observations exist for the following "
        "year/category combinations:"
    )

    print(
        duplicate_business_keys.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 16. Create analytical 2011-2021 dataset
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("13. CREATING ANALYTICAL 2011-2021 SERIES")
print("-" * 70)

# The API contains overlapping historical snapshots.
#
# Analytical selection:
#   2011 and 2021 -> report date 2021-12-31
#   2012-2020     -> report date 2022-12-31

analytical_df = df[
    (
        (df["year"].isin([2011, 2021])) &
        (df["reportDate"] == pd.Timestamp("2021-12-31"))
    )
    |
    (
        (df["year"].between(2012, 2020)) &
        (df["reportDate"] == pd.Timestamp("2022-12-31"))
    )
].copy()

analytical_df = analytical_df.sort_values(
    [
        "year",
        "registrationTypeAtEndOfYear"
    ]
).reset_index(drop=True)

print(
    f"Analytical rows: {len(analytical_df)}"
)

print(
    f"Analytical years: "
    f"{analytical_df['year'].min()} - "
    f"{analytical_df['year'].max()}"
)

print(
    f"Analytical categories: "
    f"{analytical_df['registrationTypeAtEndOfYear'].nunique()}"
)


# ------------------------------------------------------------
# 17. Broker-dealer trend
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("14. BROKER-DEALER TREND")
print("-" * 70)

broker_category = (
    "All FINRA-Registered Broker-Dealer Firms at Year End"
)

broker_df = analytical_df[
    analytical_df["registrationTypeAtEndOfYear"]
    == broker_category
].copy()

broker_df = broker_df.sort_values("year")

print(
    broker_df[
        ["year", "number_of_firms"]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 18. Broker-dealer change
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("15. BROKER-DEALER CHANGE")
print("-" * 70)

first_broker = broker_df.iloc[0]["number_of_firms"]
last_broker = broker_df.iloc[-1]["number_of_firms"]

broker_change = last_broker - first_broker

broker_change_pct = (
    broker_change / first_broker
) * 100

print(
    f"2011 firms: {first_broker:,.0f}"
)

print(
    f"2021 firms: {last_broker:,.0f}"
)

print(
    f"Absolute change: {broker_change:,.0f}"
)

print(
    f"Percentage change: {broker_change_pct:.2f}%"
)


# ------------------------------------------------------------
# 19. Broker-dealer YoY analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("16. BROKER-DEALER YOY ANALYSIS")
print("-" * 70)

broker_df["yoy_change"] = (
    broker_df["number_of_firms"]
    .diff()
)

broker_df["yoy_change_pct"] = (
    broker_df["number_of_firms"]
    .pct_change() * 100
)

print(
    broker_df[
        [
            "year",
            "number_of_firms",
            "yoy_change",
            "yoy_change_pct"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 20. Largest annual broker-dealer decline
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("17. LARGEST BROKER-DEALER ANNUAL DECLINE")
print("-" * 70)

valid_yoy = broker_df.dropna(
    subset=["yoy_change"]
)

largest_decline = valid_yoy.loc[
    valid_yoy["yoy_change"].idxmin()
]

print(
    f"Year: {int(largest_decline['year'])}"
)

print(
    f"Change: "
    f"{largest_decline['yoy_change']:,.0f} firms"
)

print(
    f"Percentage: "
    f"{largest_decline['yoy_change_pct']:.2f}%"
)


# ------------------------------------------------------------
# 21. Category-level 2011 vs 2021 comparison
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("18. CATEGORY CHANGE: 2011 VS 2021")
print("-" * 70)

category_pivot = analytical_df[
    analytical_df["year"].isin([2011, 2021])
].pivot_table(
    index="registrationTypeAtEndOfYear",
    columns="year",
    values="number_of_firms",
    aggfunc="sum"
)

category_pivot["absolute_change"] = (
    category_pivot[2021]
    - category_pivot[2011]
)

category_pivot["percentage_change"] = (
    category_pivot["absolute_change"]
    / category_pivot[2011]
) * 100

print(
    category_pivot.to_string()
)


# ------------------------------------------------------------
# 22. CAGR analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("19. CATEGORY CAGR")
print("-" * 70)

cagr_results = []

for category in sorted(
    analytical_df["registrationTypeAtEndOfYear"]
    .unique()
):

    category_data = analytical_df[
        analytical_df[
            "registrationTypeAtEndOfYear"
        ] == category
    ]

    first_value = category_data.loc[
        category_data["year"].idxmin(),
        "number_of_firms"
    ]

    last_value = category_data.loc[
        category_data["year"].idxmax(),
        "number_of_firms"
    ]

    years = (
        category_data["year"].max()
        - category_data["year"].min()
    )

    cagr = (
        (last_value / first_value)
        ** (1 / years)
        - 1
    ) * 100

    cagr_results.append(
        {
            "category": category,
            "first_year_value": first_value,
            "last_year_value": last_value,
            "cagr_pct": cagr
        }
    )

cagr_df = pd.DataFrame(cagr_results)

print(
    cagr_df.to_string(index=False)
)


# ------------------------------------------------------------
# 23. Trend direction consistency
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("20. TREND DIRECTION CONSISTENCY")
print("-" * 70)

for category in sorted(
    analytical_df[
        "registrationTypeAtEndOfYear"
    ].unique()
):

    category_data = analytical_df[
        analytical_df[
            "registrationTypeAtEndOfYear"
        ] == category
    ].sort_values("year")

    changes = (
        category_data["number_of_firms"]
        .diff()
        .dropna()
    )

    increases = (changes > 0).sum()
    decreases = (changes < 0).sum()
    unchanged = (changes == 0).sum()

    print(f"\n{category}")
    print(f"Increases: {increases}")
    print(f"Decreases: {decreases}")
    print(f"Unchanged: {unchanged}")


# ------------------------------------------------------------
# 24. Category highest and lowest years
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("21. HIGHEST AND LOWEST YEARS BY CATEGORY")
print("-" * 70)

for category in sorted(
    analytical_df[
        "registrationTypeAtEndOfYear"
    ].unique()
):

    category_data = analytical_df[
        analytical_df[
            "registrationTypeAtEndOfYear"
        ] == category
    ]

    max_row = category_data.loc[
        category_data["number_of_firms"].idxmax()
    ]

    min_row = category_data.loc[
        category_data["number_of_firms"].idxmin()
    ]

    print(f"\n{category}")

    print(
        f"Highest: "
        f"{int(max_row['year'])} "
        f"({max_row['number_of_firms']:,.0f})"
    )

    print(
        f"Lowest: "
        f"{int(min_row['year'])} "
        f"({min_row['number_of_firms']:,.0f})"
    )


# ------------------------------------------------------------
# 25. Save EDA output
# ------------------------------------------------------------

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

EDA_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "finra_eda_summary.txt"
)

# Redirect key results to a text file
with open(
    EDA_OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "FINRA INDUSTRY REGULATORY ANALYTICS - EDA SUMMARY\n"
    )

    file.write("=" * 70 + "\n\n")

    file.write(
        f"Rows: {len(df)}\n"
    )

    file.write(
        f"Columns: {len(df.columns)}\n"
    )

    file.write(
        f"Years: {df['year'].min()} - "
        f"{df['year'].max()}\n"
    )

    file.write(
        f"Categories: "
        f"{df['registrationTypeAtEndOfYear'].nunique()}\n"
    )

    file.write(
        f"Missing values: "
        f"{df.isnull().sum().sum()}\n"
    )

    file.write(
        f"Duplicate rows: "
        f"{df.duplicated().sum()}\n\n"
    )

    file.write(
        "BROKER-DEALER SUMMARY\n"
    )

    file.write("-" * 70 + "\n")

    file.write(
        f"2011: {first_broker:,.0f}\n"
    )

    file.write(
        f"2021: {last_broker:,.0f}\n"
    )

    file.write(
        f"Absolute change: {broker_change:,.0f}\n"
    )

    file.write(
        f"Percentage change: "
        f"{broker_change_pct:.2f}%\n"
    )

    file.write("\nCATEGORY CAGR\n")
    file.write("-" * 70 + "\n")

    file.write(
        cagr_df.to_string(index=False)
    )

    file.write("\n\nCATEGORY 2011 VS 2021\n")
    file.write("-" * 70 + "\n")

    file.write(
        category_pivot.to_string()
    )


# ------------------------------------------------------------
# 26. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print(
    f"\nEDA summary saved to:\n{EDA_OUTPUT}"
)

print("\nKey result:")
print(
    f"FINRA-registered broker-dealer firms: "
    f"{first_broker:,.0f} → {last_broker:,.0f}"
)

print(
    f"Overall change: "
    f"{broker_change_pct:.2f}%"
)

print("\nFINRA EDA completed successfully.")
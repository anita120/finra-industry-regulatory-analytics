import pandas as pd
import os


# --------------------------------------------------
# Locate CSV
# --------------------------------------------------

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

csv_file = os.path.join(
    project_root,
    "data",
    "raw",
    "industry_snapshot_firms_by_registration_type.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(csv_file)


# --------------------------------------------------
# Registration categories
# --------------------------------------------------

print("\n========== REGISTRATION CATEGORIES ==========\n")

categories = df[
    "registrationTypeAtEndOfYear"
].unique()

for category in categories:
    print(category)


# --------------------------------------------------
# Category counts
# --------------------------------------------------

print("\n========== CATEGORY COUNTS ==========\n")

print(
    df["registrationTypeAtEndOfYear"]
    .value_counts()
)


# --------------------------------------------------
# Years
# --------------------------------------------------

print("\n========== YEARS ==========\n")

print(
    sorted(df["year"].unique())
)


# --------------------------------------------------
# Report dates
# --------------------------------------------------

print("\n========== REPORT DATES ==========\n")

print(
    sorted(df["reportDate"].unique())
)
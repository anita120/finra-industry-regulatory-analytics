import pandas as pd
import os


# --------------------------------------------------
# File location
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
# Basic information
# --------------------------------------------------

print("\n========== DATASET OVERVIEW ==========\n")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# --------------------------------------------------
# Column names
# --------------------------------------------------

print("\n========== COLUMN NAMES ==========\n")

for column in df.columns:
    print(column)


# --------------------------------------------------
# Data types
# --------------------------------------------------

print("\n========== DATA TYPES ==========\n")

print(df.dtypes)


# --------------------------------------------------
# Missing values
# --------------------------------------------------

print("\n========== MISSING VALUES ==========\n")

missing = df.isnull().sum()

print(missing)


# --------------------------------------------------
# Duplicate records
# --------------------------------------------------

print("\n========== DUPLICATES ==========\n")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)


# --------------------------------------------------
# First 5 records
# --------------------------------------------------

print("\n========== FIRST 5 RECORDS ==========\n")

print(df.head())


# --------------------------------------------------
# Statistical summary
# --------------------------------------------------

print("\n========== SUMMARY ==========\n")

print(df.describe(include="all").transpose())
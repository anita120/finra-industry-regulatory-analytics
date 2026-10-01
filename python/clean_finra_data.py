import pandas as pd
import os


# ============================================================
# 1. Define project paths
# ============================================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

raw_file = os.path.join(
    project_root,
    "data",
    "raw",
    "industry_snapshot_firms_by_registration_type.csv"
)

processed_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(processed_folder, exist_ok=True)


# ============================================================
# 2. Load raw data
# ============================================================

df = pd.read_csv(raw_file)

print("\n========== RAW DATA ==========\n")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. Convert data types
# ============================================================

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
).astype("Int64")

df["numberOfFirms"] = pd.to_numeric(
    df["numberOfFirms"],
    errors="coerce"
)

df["reportDate"] = pd.to_datetime(
    df["reportDate"],
    errors="coerce"
)


# ============================================================
# 4. Clean text columns
# ============================================================

df["individualOrFirm"] = (
    df["individualOrFirm"]
    .astype(str)
    .str.strip()
)

df["registrationTypeAtEndOfYear"] = (
    df["registrationTypeAtEndOfYear"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 5. Validate required columns
# ============================================================

required_columns = [
    "numberOfFirms",
    "reportDate",
    "year",
    "individualOrFirm",
    "registrationTypeAtEndOfYear"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR — Missing columns:")
    print(missing_columns)
    raise SystemExit


# ============================================================
# 6. Check missing values
# ============================================================

print("\n========== MISSING VALUES ==========\n")

print(df.isnull().sum())


# ============================================================
# 7. Check duplicate rows
# ============================================================

print("\n========== DUPLICATES ==========\n")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)


# ============================================================
# 8. Check duplicate business keys
# ============================================================

business_key = [
    "year",
    "reportDate",
    "registrationTypeAtEndOfYear"
]

duplicate_keys = df.duplicated(
    subset=business_key
).sum()

print(
    "Duplicate year/report-date/category combinations:",
    duplicate_keys
)


# ============================================================
# 9. Sort data
# ============================================================

df = df.sort_values(
    [
        "year",
        "reportDate",
        "registrationTypeAtEndOfYear"
    ]
).reset_index(drop=True)


# ============================================================
# 10. Save processed data
# ============================================================

processed_file = os.path.join(
    processed_folder,
    "finra_industry_snapshot_clean.csv"
)

df.to_csv(
    processed_file,
    index=False
)


# ============================================================
# 11. Final validation
# ============================================================

print("\n========== PROCESSED DATA ==========\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nData types:")
print(df.dtypes)

print("\nYear range:")
print(
    df["year"].min(),
    "to",
    df["year"].max()
)

print("\nReport dates:")
print(
    sorted(
        df["reportDate"]
        .dt.strftime("%Y-%m-%d")
        .unique()
    )
)

print("\nRegistration categories:")
print(
    df["registrationTypeAtEndOfYear"]
    .nunique()
)

print("\nProcessed file saved to:")
print(processed_file)

print("\nFINRA data cleaning completed successfully.")
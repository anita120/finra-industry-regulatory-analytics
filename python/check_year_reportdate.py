import pandas as pd
import os

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

df = pd.read_csv(csv_file)

print("\n========== YEAR vs REPORT DATE ==========\n")

year_reportdate = (
    df.groupby(["year", "reportDate"])
      .size()
      .reset_index(name="record_count")
      .sort_values(["year", "reportDate"])
)

print(year_reportdate.to_string(index=False))


print("\n========== RECORDS BY YEAR ==========\n")

print(
    df["year"]
      .value_counts()
      .sort_index()
)


print("\n========== RECORDS BY REPORT DATE ==========\n")

print(
    df["reportDate"]
      .value_counts()
      .sort_index()
)


print("\n========== YEAR + CATEGORY COUNTS ==========\n")

year_category = (
    df.groupby(
        ["year", "registrationTypeAtEndOfYear"]
    )
    .size()
    .reset_index(name="record_count")
    .sort_values(
        ["year", "registrationTypeAtEndOfYear"]
    )
)

print(year_category.to_string(index=False))
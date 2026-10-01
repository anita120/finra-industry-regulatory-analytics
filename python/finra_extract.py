import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import json
import csv
import os


# --------------------------------------------------
# FINRA API credentials
# --------------------------------------------------

client_id = input("Enter your FINRA API Client ID: ")
client_secret = getpass("Enter your FINRA API Client Secret: ")


# --------------------------------------------------
# Step 1: Get OAuth access token
# --------------------------------------------------

token_url = (
    "https://ews.fip.finra.org/"
    "fip/rest/ews/oauth2/access_token"
    "?grant_type=client_credentials"
)

response = requests.post(
    token_url,
    auth=HTTPBasicAuth(client_id, client_secret),
    timeout=30
)


# --------------------------------------------------
# Check authentication response
# --------------------------------------------------

print("\nAuthentication response status:", response.status_code)

if response.status_code != 200:
    print("\nAuthentication failed.")
    print(response.text)
    raise SystemExit


token_data = response.json()

access_token = token_data["access_token"]

print("Authentication successful.")
print("Token type:", token_data.get("token_type"))
print("Token expires in:", token_data.get("expires_in"), "seconds")


# --------------------------------------------------
# Step 2: FINRA dataset
# --------------------------------------------------

dataset_url = (
    "https://api.finra.org/data/group/"
    "FINRA/name/IndustrySnapshotFirmsByRegistrationType"
)


headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/json"
}


params = {
    "limit": 100
}


# --------------------------------------------------
# Step 3: Request FINRA data
# --------------------------------------------------

print("\nRequesting FINRA dataset...")

dataset_response = requests.get(
    dataset_url,
    headers=headers,
    params=params,
    timeout=60
)


# --------------------------------------------------
# Check dataset response
# --------------------------------------------------

print("Dataset response status:", dataset_response.status_code)

if dataset_response.status_code != 200:
    print("\nDataset request failed.")
    print(dataset_response.text)
    raise SystemExit


data = dataset_response.json()

print("\nSUCCESS — FINRA data retrieved.")
print("Number of records returned:", len(data))


# --------------------------------------------------
# Step 4: Create raw data directory
# --------------------------------------------------

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_folder = os.path.join(
    project_root,
    "data",
    "raw"
)

os.makedirs(raw_folder, exist_ok=True)


# --------------------------------------------------
# Step 5: Save raw JSON
# --------------------------------------------------

json_file = os.path.join(
    raw_folder,
    "industry_snapshot_firms_by_registration_type.json"
)

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)


print("\nRaw JSON saved to:")
print(json_file)


# --------------------------------------------------
# Step 6: Save CSV
# --------------------------------------------------

csv_file = os.path.join(
    raw_folder,
    "industry_snapshot_firms_by_registration_type.csv"
)


if data:

    # Determine column names
    fieldnames = data[0].keys()

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(data)

    print("\nCSV saved to:")
    print(csv_file)

else:
    print("\nNo records returned. CSV was not created.")


# --------------------------------------------------
# Step 7: Display sample records
# --------------------------------------------------

print("\nFirst 5 records:\n")

for record in data[:5]:
    print(record)

print("\nFINRA extraction completed successfully.")
import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass


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
    auth=HTTPBasicAuth(client_id, client_secret)
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
# Step 2: Test a Public FINRA dataset
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
    "limit": 5
}


dataset_response = requests.get(
    dataset_url,
    headers=headers,
    params=params
)


# --------------------------------------------------
# Display dataset response
# --------------------------------------------------

print("\nDataset response status:", dataset_response.status_code)

if dataset_response.status_code == 200:
    print("\nSUCCESS — FINRA public dataset is accessible.\n")

    data = dataset_response.json()

    print("Number of records returned:", len(data))

    print("\nFirst records:")
    print(data)

else:
    print("\nDataset request failed.")
    print(dataset_response.text)
"""
File: list_assets.py
Created by: Ben Cook
Last Updated: 22 Sep 2026

This python script uses an API call to the FortiCare Asset Portal to pull a list of devices.
After pulling a subset of fields for each device, the script exports the data to a csv file.

You must create a '.env' file within the project directory and create several string variables:

  __fc_username__ - that contains your FortiCare username
  __fc_password__ - that contains your FortiCare password
  __fc_client_id__ - that contains your FortiCare client_id
  __fc_grant_type__ - that contains the type of grants for the FortiCare user

Full API documentation for FortiManager and other Fortinet products is available
on their Fortinet Developers Network website: 
https://fndn.fortinet.net/index.php
"""

import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print(
      "Dotenv dependency not met.\n" +
      "Please install with pip install dotenv" 
    )
    sys.exit(1)

try:
    import requests
except ImportError:
    print(
        "Requests dependency not met.\n" +
        "Please install with pip install requests"
    )
    sys.exit(1)

try:
    import json
except ImportError:
    print(
        "JSON dependency not met.\n" +
        "Please install with pip install json"
    )
    sys.exit(1)

try:
    import csv
except ImportError:
    print(
        "Requests dependency not met.\n" +
        "Please install with pip install csv")
    sys.exit(1)

from datetime import datetime, timezone

load_dotenv()
fc_username = os.getenv("fc_username")
fc_password = os.getenv("fc_password")
fc_client_id = os.getenv("fc_client_id")

ftnt_fac_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

ftnt_fac_headers = {
    "Content-Type": "application/json"
}

ftnt_fac_payload = {
    "username": fc_username,
    "password": fc_password,
    "client_id": fc_client_id,
    "grant_type": "password"
}

ftnt_fac_response = requests.post(ftnt_fac_url, headers=ftnt_fac_headers,json=ftnt_fac_payload,allow_redirects=False)

ftnt_fac_access_token = ftnt_fac_response.json()['access_token']
ftnt_fac_refresh_token = ftnt_fac_response.json()['refresh_token']

ftnt_asset_url = "https://support.fortinet.com/ES/api/registration/v3/products/list"

ftnt_asset_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ftnt_fac_access_token
}

# Needs either serialNumber (exact or pattern) or expireBefore as required values; could make this into a function and loop

ftnt_asset_payload = {
# "accountId": 854651
  "serialNumber": "FGT", # specific or pattern like FGT, FGR, FS, FSR, etc.
  # "productModel": "FortiGate 90D***", 
  # "expireBefore": "2019-01-20T10:11:11-8:00",
  # "status": "Registered"
}

ftnt_asset_response = requests.post(ftnt_asset_url,headers=ftnt_asset_headers,json=ftnt_asset_payload,allow_redirects=False)

# return a dictionary
data = ftnt_asset_response.json()

# grabs just the assets section of the return
data_dict = data['assets']

assets = []

# choose which fields specifically to use when filtering down the data_dict
data_keys = ['status', 'serialNumber', 'registrationDate', 'productModel', 'isDecommissioned', 'description']

for item in data_dict:
    new_data_dict = {k: item[k] for k in data_keys if k in item}
    assets.append(new_data_dict)

# print(json.dumps(assets,indent=4,sort_keys=True))

csv_fields = []

for key in assets[0]:
    csv_fields.append(key)

with open('fc-devices.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=csv_fields)
    writer.writeheader()
    writer.writerows(assets)

"""
File: bulk_registration.py
Created by: Ben Cook
Last Updated: 24 Sep 2026

This python script uses an API call to the FortiCare Asset Portal to register a list of licenses.

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

ftnt_asset_url = "https://support.fortinet.com/ES/api/registration/v3/licenses/register/"

ftnt_asset_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ftnt_fac_access_token
}

def query_asset_portal(license):
    # Needs either serialNumber (exact or pattern) or expireBefore as required values

    ftnt_asset_payload = {
    # "accountId": 854651,
    # "serialNumber": "", 
    # "description": "",
    # "additionalInfo": "",
      "isGovernment": False,
      "licenseRegistrationCode": license
    }

    try:
        ftnt_asset_response = requests.post(ftnt_asset_url,headers=ftnt_asset_headers,json=ftnt_asset_payload,allow_redirects=False)
    except:
        ftnt_asset_response.raise_for_status()

    # return a dictionary
    data = ftnt_asset_response.json()
    print(json.dumps(data,indent=4,sort_keys=True))

    if data['status'] == -1:
        print(data['error']['message'] + " \n Exiting with error.")
        sys.exit(1)

    elif data['status'] == -2:
        print("License " + item + " " + data['error']['message'] + " \n Exiting with error.")
        sys.exit(1)

    elif data['status'] == -30:
        print(data['error']['message'] + "\n Exiting with error.")
        sys.exit(1)

    elif data['status'] != 0:
        print(data['error']['message'] + "\n Exiting with error.")
        sys.exit(1)


licenses = ["E4711-0UFNB-QEKED-VKWNZ-RNQ6HC"]

for item in licenses:
    query_asset_portal(item)

print("A total of ", len(licenses), " license/s were registered successfully. Exiting.")
sys.exit(0)
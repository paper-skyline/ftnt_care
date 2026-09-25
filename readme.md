# Purpose

## Asset Management Pre-Requisites

1. Create an API user through the IAM portal
2. Obtain an OAuth token
3. Include the OAuth token in your API requests

## FortiCloud Services

Check out [Fortinet's Document Library](https://docs.fortinet.com/document/forticloud/26.3.a/identity-access-management-iam/927656/api-users) if you need help creating an API Administrator, Access Profile, Token, and so on.

## Installation

After cloning the github repository, move to the directory in a terminal and run: `pipenv install`

If you don't have *pipenv* installed, from your terminal run: `pip install pipenv`

## Script Usage

After cloning the project, create a __.env__ file within the directory. Define and populate the following string variables with details for your environment:

  __fc_username__ - that contains your FortiCare username

  __fc_password__ - that contains your FortiCare password

  __fc_client_id__ - that contains your FortiCare client_id
  
  __fc_grant_type__ - that contains the type of grants for the FortiCare user

From the project directory, install the dependencies by running `pipenv install` and then run the script with your virtual environment by running `pipenv run python list_assets.py`

After the script completes, you should now have a *fc-devices.csv* file in your directory that contains the selected information for each device.

## Disclaimer

__*Use at your own risk*__

These example configurations were a learning tool for me to figure out what works for what I was trying to do, what didn't work, and maybe even a little bit as to why. I make no claims that this is the best way, or even the correct way, to configure devices utilizing this technology. What worked for me in a certain situation may not work for you, etc. I encourage you to take the time to learn and try these things out yourself and make your own judgments.

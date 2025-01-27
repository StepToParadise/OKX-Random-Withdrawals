import base64
import hashlib
import hmac
import json
import requests
from datetime import datetime, timezone
from config import CONFIG

API_KEY = CONFIG['API_KEY']
API_SECRET_KEY = CONFIG['API_SECRET_KEY']
API_PASSPHRASE = CONFIG['API_PASSPHRASE']

timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

request_path = '/api/v5/asset/currencies'
method = 'GET'

body = ''

pre_sign = timestamp + method + request_path + body

signature = base64.b64encode(hmac.new(API_SECRET_KEY.encode(), pre_sign.encode(), hashlib.sha256).digest()).decode()

headers = {
    'OK-ACCESS-KEY': API_KEY,
    'OK-ACCESS-SIGN': signature,
    'OK-ACCESS-TIMESTAMP': timestamp,
    'OK-ACCESS-PASSPHRASE': API_PASSPHRASE,
    'Content-Type': 'application/json'
}

url = f"https://www.okx.com{request_path}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    #print("Response data:", json.dumps(data, indent=4))

    if isinstance(data, dict) and 'data' in data:
        assets = []

        for asset in data['data']:
            if isinstance(asset, dict):
                asset_info = {
                    'name': asset.get('name', 'N/A'),
                    'chain': asset.get('chain', 'N/A'),
                    'fee': asset.get('fee', 'N/A')
                }
                assets.append(asset_info)

        #for asset in assets:
        #    print(f"Name: {asset['name']}, Chain: {asset['chain']}, Fee: {asset['fee']}")

        with open('assets_info.json', 'w') as json_file:
            json.dump(assets, json_file, indent=4)
            print('Assets dumped to assets_info.json')

    else:
        print("Response data does not contain expected 'data' key.")
else:
    print(f"Error: {response.status_code}, Response: {response.text}")
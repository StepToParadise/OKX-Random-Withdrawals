import json
import random
import time
import os
from decimal import Decimal, ROUND_DOWN
from okx import Funding
from typing import List
from config import CONFIG

def load_addresses(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_minimum_fee(funding: Funding, token: str, network: str) -> Decimal:
    withdrawal_info = funding.get_currencies()
    try:
        response = funding.get_currencies()        
        if 'data' not in response or not isinstance(response['data'], list):
            raise ValueError(f"Invalid response structure: {response}")
    except Exception as e:
        raise Exception(f"Failed to retrieve minimum fee for token {token} on network {network}: {e}")
    if 'data' in withdrawal_info:
        for asset in withdrawal_info['data']:
            if 'ccy' in asset and asset['ccy'] == token:
                if 'chains' in asset:
                    for chain in asset['chains']:
                        if 'chain' in chain and chain['chain'] == network:
                            return Decimal(chain.get('minFee', 0))
    else:
        print("Error: 'data' key not found in withdrawal_info.")

def generate_random_amount(min_amount: float, max_amount: float, decimals: int) -> Decimal:
    amount = random.uniform(min_amount, max_amount)
    return Decimal(amount).quantize(Decimal(f'1e-{decimals}'), rounding=ROUND_DOWN)

def withdraw_token(funding: Funding, token: str, network: str, address: str, amount: Decimal, fee: Decimal):
    response = funding.withdrawal(
        ccy=token,
        amt=str(amount),
        dest='4',
        toAddr=address,
        chain=network
    )
    if response['code'] != '0':
        raise Exception(f"Withdrawal failed: {response}")
    return response['data'][0]

def save_withdrawal_log(log_data: dict, file_name: str):
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data.append(log_data)
        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)
    
    except Exception as e:
        print(f"Error saving log: {e}")

def load_processed_addresses(file_path: str) -> set:
    try:
        with open(file_path, 'r') as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_processed_addresses(file_path: str, addresses: set):
    with open(file_path, 'w') as file:
        json.dump(list(addresses), file, indent=4)

def main():
    os.makedirs('logs', exist_ok=True)
    log_filename = os.path.join(
        'logs', 
        time.strftime("%Y-%m-%d_%H-%M") + '.json'
    )
    
    addresses = load_addresses('addresses.txt')
    random.shuffle(addresses)
    
    processed_addresses = load_processed_addresses('processed_addresses.json')
    
    funding = Funding.FundingAPI(
        api_key=CONFIG['API_KEY'],
        api_secret_key=CONFIG['API_SECRET_KEY'],
        passphrase=CONFIG['API_PASSPHRASE'],
        use_server_time=False,
        flag='0'
    )
    
    for address in addresses:
        if address in processed_addresses:
            print(f"Address {address} already processed. Skipping.")
            continue
        
        network_name = random.choice(CONFIG['Network'])
        network = f"{CONFIG['Token']}-{network_name}"
        
        try:
            fee = get_minimum_fee(funding, CONFIG['Token'], network)
            amount = generate_random_amount(
                CONFIG['Amount'][0], 
                CONFIG['Amount'][1], 
                CONFIG['Decimals']
            )
            
            result = withdraw_token(
                funding, 
                CONFIG['Token'], 
                network, 
                address, 
                amount, 
                fee
            )
            
            log_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "address": address,
                "network": network,
                "amount": str(amount),
                "fee": str(fee),
                "withdrawal_id": result['wdId']
            }
            
            save_withdrawal_log(log_data, log_filename)
            print(f"Withdrawal successful: {log_data}")
            
            processed_addresses.add(address)
            save_processed_addresses('processed_addresses.json', processed_addresses)
            
            sleep_time = random.randint(CONFIG['Sleep'][0], CONFIG['Sleep'][1])
            print(f"Sleeping for {sleep_time} seconds...\n")
            time.sleep(sleep_time)
        
        except Exception as e:
            print(f"Error processing {address} on {network}: {str(e)}")
    
    print("All addresses processed.")

if __name__ == "__main__":
    main()
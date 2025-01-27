CONFIG = {
    "Token": "ETH",                 # Cryptocurrency to withdraw
    "Network": [                    # Supported networks
        "Arbitrum One", 
        "Base", 
        "Optimism", 
        "Linea"
    ],
    "Amount": [0.001, 0.01],        # Min/Max withdrawal amounts
    "Decimals": 7,                  # Decimal precision
    "Sleep": [600, 1800],           # Min/Max delay between withdrawals (seconds)
    "API_KEY": "your_api_key",      # From OKX API
    "API_SECRET_KEY": "your_secret_key",
    "API_PASSPHRASE": "your_passphrase",
}

# Tokens and available networks described in asset_info.json
# You can actualize them via running networks.py
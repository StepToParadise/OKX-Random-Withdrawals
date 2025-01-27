# OKX Automated Withdrawal Bot

A Python script for automated cryptocurrency withdrawals to multiple addresses via OKX exchange API.

## Features

- 🚀 Automated withdrawals with randomized parameters
- 🔀 Random network selection from configured list
- ⚖️ Customizable amount ranges with decimal precision
- ⏳ Configurable random delays between transactions
- 📝 Automatic logging of all transactions
- ✅ Prevention of duplicate address processing
- 🔒 Secure API key management

## Requirements

- Python 3.8+
- OKX API keys (with withdrawal permissions)
- Python packages:
  - `okx`
  - `python-okx` (recommended)
  - `requests`

## Installation

1. Clone repository:
    ```bash
    git clone https://github.com/StepToParadise/OKX-Random-Withdrawals.git
    cd okx-withdrawal-bot

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Setup necessary files:
    - `addresses.txt`
    - `config.py`

4. Setup config.py

## Running

- After successful setup run:
    ```bash
    python withdraw.py

## Donate

- EVM: `0x3124Be9C360d4931bF9937Da4DB3507899F0f7EB`
- SOL: `9htc1cTKmHwBMwQZSgZJFQNz7nKiUaC9G5x1ZDt8oXHP`

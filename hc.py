import requests
import time
import json
import datetime
import os
import random
import sys

# Function to read authorization tokens from data.txt
def read_authorizations(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to perform the POST request
def collect_coin(auth_token, collect_amount, hash_code, collect_seq_no):
    url = "https://api.holdcoin.xyz/miniapps/api/user_game/collectCoin"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "collectAmount": collect_amount,
        "hashCode": hash_code,
        "collectSeqNo": collect_seq_no
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.status_code, response.json()
    except json.JSONDecodeError:
        return response.status_code, response.text

# Function to display countdown timer
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f'\rCountdown: {timer}', end="")
        time.sleep(1)
        seconds -= 1
    print("\rCountdown: 00:00")

def main():
    auth_tokens = read_authorizations('data.txt')
    total_accounts = len(auth_tokens)

    print(f'Total accounts: {total_accounts}')
    
    for idx, token in enumerate(auth_tokens, start=1):
        print(f'Processing account {idx}/{total_accounts}')
        
        collect_amount = random.randint(100, 200)  # Random collect amount
        hash_code = ''.join(random.choices('abcdef0123456789', k=32))  # Random hash code
        collect_seq_no = random.randint(1, 10)  # Random collect sequence number
        
        status_code, response_data = collect_coin(token, collect_amount, hash_code, collect_seq_no)
        
        if status_code == 200:
            print(f'Account {idx} processed successfully: {response_data}')
        else:
            print(f'Failed to process account {idx}: {response_data}')
        
        time.sleep(5)  # Wait for 5 seconds before switching to the next account
    
    print('All accounts processed. Starting 1-hour countdown.')
    countdown_timer(3600)
    
    # Restart the script
    print('Restarting script.')
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    main()

import requests
import time
import json
import os
import random
import sys
import hashlib

# Function to read authorization tokens and hash codes from data.txt
def read_authorizations(file_path):
    auth_data = []
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        for i in range(0, len(lines), 2):
            auth_token = lines[i]
            hash_code = lines[i+1] if i+1 < len(lines) else ''
            auth_data.append((auth_token, hash_code))
    return auth_data

# Function to generate a new hashCode based on an existing hashCode
def generate_new_hash_code(existing_hash_code):
    random_suffix = ''.join(random.choices('abcdef0123456789', k=8))
    new_hash_code = hashlib.sha256((existing_hash_code + random_suffix).encode()).hexdigest()
    return new_hash_code

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
    auth_data = read_authorizations('data.txt')
    total_accounts = len(auth_data)

    print(f'Total accounts: {total_accounts}')
    
    for idx, (token, existing_hash_code) in enumerate(auth_data, start=1):
        print(f'Processing account {idx}/{total_accounts}')
        
        initial_collect_seq_no = random.randint(1, 10)  # Initial collect sequence number
        collect_amount = random.randint(100, 300)  # Random collect amount between 100 and 300
        times_to_collect = random.randint(5, 10)  # Random number of times to perform collect_coin
        
        for attempt in range(times_to_collect):
            collect_seq_no = initial_collect_seq_no + attempt
            new_hash_code = generate_new_hash_code(existing_hash_code)
            
            status_code, response_data = collect_coin(token, collect_amount, new_hash_code, collect_seq_no)
            
            if status_code == 200:
                print(f'Account {idx} attempt {attempt+1}/{times_to_collect} processed successfully: {response_data}')
            else:
                print(f'Failed to process account {idx} attempt {attempt+1}/{times_to_collect}: {response_data}')
            
            time.sleep(5)  # Wait for 5 seconds before the next attempt
        
        time.sleep(5)  # Wait for 5 seconds before switching to the next account
    
    print('All accounts processed. Starting 1-hour countdown.')
    countdown_timer(3600)
    
    # Restart the script
    print('Restarting script.')
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    main()

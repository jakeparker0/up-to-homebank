
import requests
import os
import json


def list_accounts(access_token, page_size=None):
    url = "https://api.up.com.au/api/v1/accounts"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page[size]": page_size} if page_size else {}
    response = requests.get(url, headers=headers, params=params)
    # for acc in response.json()['data']:
    #     print(acc['attributes']['displayName'][1:])
    return response.json()


def retrieve_account(access_token, account_id):
    url = f"https://api.up.com.au/api/v1/accounts/{account_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def list_transactions(access_token, params = {}):
    url = "https://api.up.com.au/api/v1/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)
    transactions = response.json()['data']
    next_page = response.json()['links']['next']
    while next_page:
        print(len(transactions))
        response = requests.get(next_page, headers=headers)
        transactions += response.json()['data']
        next_page = response.json()['links']['next']
    json.dump(transactions, open('transactions.json', 'w'), indent=4) 
    return transactions

def list_transactions_by_account(access_token, account_name, output_qif = False, params = {}):
    accounts = list_accounts(access_token)['data']
    account_id = None
    for acc in accounts:
        if acc['attributes']['displayName'].endswith(account_name):
            account_id = acc['id']
            break
    if account_id is None:
        return None
    print(account_name)
    url = f"https://api.up.com.au/api/v1/accounts/{account_id}/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)
    transactions = response.json()['data']
    next_page = response.json()['links']['next']
    while next_page:
        
        response = requests.get(next_page, headers=headers)
        transactions += response.json().get('data', [])
        next_page = response.json()['links']['next']
    json.dump(transactions, open(f'{account_name}.json', 'w'), indent=4) 
    print(len(transactions))
    if output_qif:
        write_transactions_to_qif(transactions, f'{account_name}.qif')
    return transactions


def retrieve_transaction(access_token, transaction_id):
    url = f"https://api.up.com.au/api/v1/transactions/{transaction_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def list_tags(access_token):
    url = "https://api.up.com.au/api/v1/tags"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def retrieve_tag(access_token, tag_id):
    url = f"https://api.up.com.au/api/v1/tags/{tag_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def add_tag_to_transaction(access_token, transaction_id, tag):
    url = f"https://api.up.com.au/api/v1/transactions/{transaction_id}/relationships/tags"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"data": [{"type": "tags", "id": tag}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def write_transactions_to_qif(transactions, qif_file_path):
    with open(qif_file_path, 'w', encoding="utf-8") as file:
        # Write QIF header for bank transactions
        file.write("!Type:Bank\n")
        
        for transaction in transactions:
            date = transaction['attributes']['createdAt'][:10]  # Use the date part
            amount = transaction['attributes']['amount']['value']
            description = transaction['attributes']['description'] or ''
            tags = ",".join(tag['id'] for tag in transaction['relationships']['tags']['data'])
            
            # Write the transaction details
            try:
                file.write(f"D{date}\n")  # Date
            except Exception as e:
                print(date)
            try:
                file.write(f"T{amount}\n")  # Amount
            except Exception as e:
                print(amount)
            try:
                file.write(f"M{description}\n")  # Description
            except Exception as e:
                print(description)
            if tags:
                file.write(f"L{tags}\n")  # Tags (as categories in QIF)
            file.write("^\n")  # End of the transaction

import csv

def write_transactions_to_csv(transactions, csv_file_path):
    # Define the headers for the CSV file
    headers = ["date", "amount", "account", "st", "category", "tags", "description"]
    
    # Convert transactions to CSV format
    rows = []
    for transaction in transactions:
        date = transaction['attributes']['createdAt'][:10]  # Use just the date part
        amount = transaction['attributes']['amount']['value']
        account = "13"
        st = "1"
        category = ""  # Category left empty as per instructions
        tags = ",".join(tag['id'] for tag in transaction['relationships']['tags']['data'])
        description = transaction['attributes']['description']
        rows.append([date, amount, account, st, category, tags, description])

    # Write to CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write rows
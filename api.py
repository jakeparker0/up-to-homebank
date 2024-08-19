from dotenv import load_dotenv
import requests
import os


load_dotenv()

access_token = os.environ.get('UP_KEY')

def list_accounts(access_token, page_size=None):
    url = "https://api.up.com.au/api/v1/accounts"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page[size]": page_size} if page_size else {}
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def retrieve_account(access_token, account_id):
    url = f"https://api.up.com.au/api/v1/accounts/{account_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def list_transactions(access_token, page_size=None):
    url = "https://api.up.com.au/api/v1/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page[size]": page_size} if page_size else {}
    response = requests.get(url, headers=headers, params=params)
    return response.json()


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


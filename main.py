
from dotenv import load_dotenv
import datetime
from api import list_transactions_by_account, list_accounts
import os
import json
import re

load_dotenv()

access_token = os.environ.get('UP_KEY')

def append_transactions_to_file(transactions, file_path):
    def days_since_year_0(date_str):
        try:
            date_obj = datetime.datetime.fromisoformat(date_str[:-6])
            return (date_obj - datetime.datetime(1, 1, 1)).days
        except TypeError:
            print(date_str)

    # Read existing file content and remove </homebank>
    with open(file_path, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write(content.replace('</homebank>', '').rstrip())
        sorted_transactions = sorted(transactions, key=lambda x: x['attributes']['createdAt'])
        # Append new transactions
        for transaction in sorted_transactions:
            try:
                date = days_since_year_0(transaction['attributes']['createdAt'])
                amount = transaction['attributes']['amount']['value']
                account = "13"
                st = "1"
                category = "193" if float(amount) < 0 else "194"
                tags = ",".join(tag['id'] for tag in transaction['relationships']['tags']['data'])

                file.write(f'\n<ope date="{date}" amount="{amount}" account="{account}" st="{st}" category="{category}" wording="{transaction["attributes"]["description"]}"')
                if tags:
                    file.write(f' tags="{tags}"')
                file.write('/>')
            except Exception as e:
                print("error with ",transaction)
        # Re-add the closing </homebank> tag
        file.write('\n</homebank>')






# # Sample usage:
#response = list_transactions(access_token, params={"filter[since]": '2024-09-01T00:00:00+10:00'})
# write_transactions_to_csv(response, "Finances.csv")
#append_transactions_to_file(response, "Finances.xhb")



# Sample usage:
# response = list_transactions(access_token)
#write_transactions_to_qif(response, "transactions.qif")

extract_date = '2025-03-03T00:00:00+10:00'

list_transactions_by_account(access_token, "Spending", output_qif=True, params={"filter[since]": extract_date})
list_transactions_by_account(access_token, "2Up Spending", output_qif=True, params={"filter[since]": extract_date})
list_transactions_by_account(access_token, '"MacBook Air 13" (M3) 8 Core CPU 8 Core GPU 16/256 Midnight', output_qif=True, params={"filter[since]": extract_date})
list_transactions_by_account(access_token, "Clothes", output_qif=True, params={"filter[since]": extract_date})
list_transactions_by_account(access_token, "Hobby", output_qif=True, params={"filter[since]": extract_date})
list_transactions_by_account(access_token, "Investment", output_qif=True, params={"filter[since]": extract_date})
import requests
from dotenv import load_dotenv
import os
import uuid

class TransferWise:

    def __init__(self):
        load_dotenv()        
        self.__API_TOKEN = os.getenv("API_TOKEN")
    

    def get_recipients(self, target_currency):
        # url = f"https://api.sandbox.transferwise.tech/v1/accounts?currency={self.from_currency}"
        url = f"https://api.transferwise.com/v1/accounts?currency={target_currency}"

        headers = {"Authorization": f"Bearer {self.__API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)

        return response.json()


    def get_profile_id(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/profiles"
        url = f"https://api.transferwise.com/v1/profiles"
        headers = {"Authorization": f"Bearer {self.__API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)


        return response.json()

    

    def quote(self, source_currency, target_currency, profile_id, amount):
        # url = f"https://api.sandbox.transferwise.tech/v1/quotes"
        url = f"https://api.transferwise.com/v1/quotes"

        headers = {"Authorization": f"Bearer {self.__API_TOKEN}",
                   "Content-Type": "application/json"}
        data = {"profile": profile_id,
                "source": source_currency,
                "target": target_currency,
                "rateType": "FIXED",
                "sourceAmount": amount,
                "type": "BALANCE_PAYOUT"
                }

        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)

        return response.json()
    

    def create_transfer(self, recipient, quote_id):
        # url = f"https://api.sandbox.transferwise.tech/v1/transfers"
        url = f"https://api.transferwise.com/v1/transfers"

        headers = {"Authorization": f"Bearer {self.__API_TOKEN}",
                   "Content-Type": "application/json"}
        data = {
            "targetAccount": recipient["id"],
            "quote": quote_id,
            "customerTransactionId": str(uuid.uuid4()),
            "details": {
                "reference": "Sent automatically by AutoWise"
            }
        }

        response = requests.post(url=url, headers=headers, json=data).json()

        return response
    

    def cancel_transfer(self, transfer_id):
        # url = f"https://api.sandbox.transferwise.tech/v1/transfers/{transfer_id}/cancel"
        url = f"https://api.transferwise.com/v1/transfers/{transfer_id}/cancel"
        headers = {"Authorization": f"Bearer {self.__API_TOKEN}"}

        response = requests.put(url=url, headers=headers).json()

        return response
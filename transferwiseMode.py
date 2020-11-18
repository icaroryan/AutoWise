# https://api-docs.transferwise.com/#transferwise-api
# https://github.com/tedchou12/transferwise/blob/a83d826ec943d082e666e02683c90cd760bc94f8/tw_api.py


# email: yurdemiydi@nedoz.com

from dotenv import load_dotenv
import os, requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")

class TransferWise:
    # Class Variables

    def __init__(self, from_currency, to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency


    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
    def get_rate(self):
        url = f"https://transferwise.com/gb/currency-converter/{self.to_currency}-to-{self.from_currency}-rate"

        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'lxml')
        span = soup.body.find("span", attrs={"class": "text-success"})
        
        # rate = div.select_one(".inlineblock.arial_26").get_text()
        rate = float(span.get_text())
        # fluctuation = div.select_one(".parentheses.arial_20").get_text()

        rate = round(rate, 4)

        return rate















        """
        Output: Rate
        """
        # url = f"https://api.sandbox.transferwise.tech/v1/rates?source={self.to_currency}&target={self.from_currency}"
        url = f"https://api.transferwise.com/v1/rates?source={self.to_currency}&target={self.from_currency}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)
        rate = format(response.json()[0]['rate'], '.4f')

        return rate

    
    def set_threshold(self, threshold):
        self.threshold = threshold


    def set_amount(self, amount):
        self.amount = amount

    def get_threshold(self):
        return self.threshold

    
    def get_profile_id(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/profiles"
        url = f"https://api.transferwise.com/v1/profiles"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)

        profile_n = 0
        
        response_json = response.json()
        if len(response_json) > 1:
            print("-- Profiles --")
            for i, profile in enumerate(response_json):
                try:
                    print(f"{i + 1}: {profile['details']['firstName']} {profile['details']['lastName']} > Type: {profile['type']} (ID: {profile['id']})")
                except KeyError:
                    print(f"{i + 1}: {profile['details']['name']} > Type: {profile['type']} (ID: {profile['id']})")


            option = int(input("\nWe noticed you have more than one profile in your account. \nEnter the profile number you want to send money from: "))
            print()
            profile_n = option - 1

        return response_json[profile_n]["id"]

    def set_profile_id(self, profile_id):
        self.profile_id = profile_id


    def quote(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/quotes"
        url = f"https://api.transferwise.com/v1/quotes"
        headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
        data = {"profile": self.profile_id, 
            "source": self.from_currency, 
            "target": self.to_currency, 
            "rateType": "FIXED", 
            "sourceAmount": self.amount, 
            "type": "BALANCE_PAYOUT"
            }

        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)

        response_json = response.json()

        self.quote_id = response_json['id']

        self.sourceAmount = response_json['sourceAmount']
        targetAmount = response_json['targetAmount']
        fee = response_json['fee']
        commercial_rate = format((sourceAmount - fee) / targetAmount, '.4f')
        vet = format(sourceAmount / targetAmount, '.4f')

        createdTime = response_json['createdTime']
        objDate = datetime.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        createdTime = objDate.strftime("%B %d, %Y %H:%M:%S")

        

        print(f"\nYou send {self.sourceAmount} {self.from_currency} >> Recipient gets {targetAmount} {self.to_currency}\nCommercial rate: {commercial_rate}   ||   That's 1 {self.to_currency} = {vet} {self.from_currency} Effective Rate (VET)")
        

    def get_recipients(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/accounts?currency={self.from_currency}"
        url = f"https://api.transferwise.com/v1/accounts?currency={self.to_currency}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code >= 400 and response.status_code <= 499:
            exit(response.text)

        return response.json()

    
    def set_recipient(self, recipient):
        self.recipient = recipient

    
    def create_transfer(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/transfers"
        url = f"https://api.transferwise.com/v1/transfers"

        headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
        data = {
            "targetAccount": self.recipient["id"],
            "quote": self.quote_id,
            "customerTransactionId": str(uuid.uuid4()),
            "details": {
                "reference": "Sent automatically by AutoWise"
            }
        }

        response = requests.post(url=url, headers=headers, json=data)
        response_json = response.json()

        created_date = response_json["created"]
        rate = response_json["rate"]
        # source_value = response_json["sourceValue"]
        source_Currency = response_json["sourceCurrency"]
        target_value =  round(source_value * rate, 2)
        # target_value =  format(source_value * rate, '.2f')
        target_Currency = response_json["targetCurrency"]


        print(f"\nTransfer created successfully! {target_value} {target_Currency}   ({self.sourceAmount} {source_Currency})     [{created_date}]")

    def send_money(self):
        self.quote()
        self.create_transfer()

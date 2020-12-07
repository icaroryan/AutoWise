# https://api-docs.transferwise.com/#transferwise-api
# https://github.com/tedchou12/transferwise/blob/a83d826ec943d082e666e02683c90cd760bc94f8/tw_api.py


# email: yurdemiydi@nedoz.com

from dotenv import load_dotenv
import os
import requests
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

        self.last_transfer = {}
        self.last_idle_transfer = {}
        self.thresholds = []

    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates

    def get_rate(self):
        url = f"https://transferwise.com/gb/currency-converter/{self.to_currency}-to-{self.from_currency}-rate"

        while True:
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(resp.text, 'lxml')
            span = soup.body.find("span", attrs={"class": "text-success"})

            # rate = div.select_one(".inlineblock.arial_26").get_text()
            try:
                rate = float(span.get_text())
            # Make sure the page is returning a value
            except AttributeError:
                continue
            else:
                break
            # fluctuation = div.select_one(".parentheses.arial_20").get_text()

        rate = round(rate, 4)
        return rate

    def set_threshold(self, threshold):
        threshold = float(threshold)
        # 0.3% more
        upper_bound = round(threshold * 1.003, 4)
        # 0.3% less
        lower_bound = round(threshold * 0.998, 4)
        self.thresholds.extend([upper_bound, threshold, lower_bound])

    def set_amount(self, amount):
        self.amount = amount

    def get_threshold(self):
        return self.thresholds

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
                    print(
                        f"{i + 1}: {profile['details']['firstName']} {profile['details']['lastName']} > Type: {profile['type']} (ID: {profile['id']})")
                except KeyError:
                    print(
                        f"{i + 1}: {profile['details']['name']} > Type: {profile['type']} (ID: {profile['id']})")

            option = int(input(
                "\nWe noticed you have more than one profile in your account. \nEnter the profile number you want to send money from: "))
            print()
            profile_n = option - 1

        return response_json[profile_n]["id"]

    def set_profile_id(self, profile_id):
        self.profile_id = profile_id

    def quote(self):

        # url = f"https://api.sandbox.transferwise.tech/v1/quotes"
        url = f"https://api.transferwise.com/v1/quotes"
        headers = {"Authorization": f"Bearer {API_TOKEN}",
                   "Content-Type": "application/json"}
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

        response = response.json()
        ############
        if self.last_transfer:
            self.last_idle_transfer = self.last_transfer.copy()

        self.quote_id = response['id']

        self.sourceAmount = response['sourceAmount']
        targetAmount = response['targetAmount']
        fee = response['fee']

        commercial_rate = format(
            (self.sourceAmount - fee) / targetAmount, '.4f')
        self.last_transfer["rate"] = commercial_rate

        vet = format(self.sourceAmount / targetAmount, '.4f')

        createdTime = response['createdTime']
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

    def get_recipient(self):
        return self.recipient

    def create_transfer(self):
        # url = f"https://api.sandbox.transferwise.tech/v1/transfers"
        url = f"https://api.transferwise.com/v1/transfers"

        headers = {"Authorization": f"Bearer {API_TOKEN}",
                   "Content-Type": "application/json"}
        data = {
            "targetAccount": self.recipient["id"],
            "quote": self.quote_id,
            "customerTransactionId": str(uuid.uuid4()),
            "details": {
                "reference": "Sent automatically by AutoWise"
            }
        }

        response = requests.post(url=url, headers=headers, json=data).json()

        self.last_transfer["id"] = response["id"]

        created_date = response["created"]
        rate = response["rate"]
        source_value = response["sourceValue"]
        source_Currency = response["sourceCurrency"]

        target_value = round(source_value * rate, 2)
        target_Currency = response["targetCurrency"]

        print(
            f"\nTransfer created successfully! \033[1;32;40m{target_value} {target_Currency}   \033[0;37;40m({self.sourceAmount} {source_Currency})     [{created_date}]")

        if self.last_idle_transfer:
            self.cancel_transfer()

        print("----------------------------------------------------------------------------------------------\n")

    def send_money(self):
        self.quote()
        self.create_transfer()

    def cancel_transfer(self):
        
        # transfer_id = self.last_transfer["id"]
        transfer_id = self.last_idle_transfer["id"]
        # transfer_rate = self.last_transfer["rate"]
        transfer_rate = self.last_idle_transfer["rate"]

        print(
            f"\nSince a lower threshold was reached, we're cancelling the previous transfer")

        url = f"https://api.transferwise.com/v1/transfers/{transfer_id}/cancel"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.put(url=url, headers=headers).json()

        try:
            print(
                f"The transfer created on {response['created']} was successfully canceled (Commercial Rate: {transfer_rate})")
        except KeyError:
            print(
                f"Something went wrong while canceling the transfer. Error: {response['error']}")

        else:
            self.last_idle_transfer = {}

# https://api-docs.transferwise.com/#transferwise-api
# https://transferwise.com/help/articles/2958107/how-can-my-business-use-the-transferwise-api


# email: yurdemiydi@nedoz.com

from dotenv import load_dotenv
import os, requests

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")

class TransferWise:
    # Class Variables

    def __init__(self, from_currency, to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency


    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
    def get_rate(self):
        """
        Output: Rate
        """
        url = f"https://api.transferwise.com/v1/rates?source={self.from_currency}&target={self.to_currency}"
        # url = f"https://api.sandbox.transferwise.tech/v1/rates?source={self.from_currency}&target={self.to_currency}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code == 401:
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

        print("Getting your profile ID..")
        response = requests.get(url=url, headers=headers)
        if response.status_code == 401:
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


            option = int(input("\nWe noticed you have more than one profile in your account. Enter the profile number you want to send money from: "))
            profile_n = option - 1

        return response_json[profile_n]["id"]


    def quote(self):
        pass

    def get_recipients(self):
        url = f"https://api.transferwise.com/v1/accounts?currency={self.from_currency}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code == 401:
            exit(response.text)

        return response.json()

    
    def set_recipient(self, recipient):
        self.recipient = recipient


    def send_money(self):
        pass

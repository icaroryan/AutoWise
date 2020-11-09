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
        rate = format(response.json()[0]['rate'], '.4f')

        return rate

    
    def set_threshold(self, threshold):
        self.threshold = threshold


    def get_threshold(self):
        return self.threshold


    def get_recipients(self):
        url = f"https://api.transferwise.com/v1/accounts?currency={self.from_currency}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=url, headers=headers)

        return response.json()

    
    def set_recipient(self, recipient):
        self.recipient = recipient


    def send_money(self):
        pass
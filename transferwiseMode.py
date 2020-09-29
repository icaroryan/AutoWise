# https://api-docs.transferwise.com/#transferwise-api
# https://transferwise.com/help/articles/2958107/how-can-my-business-use-the-transferwise-api

from dotenv import load_dotenv
import os, requests

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")

class Currency:
    # Class Variables
    url = None

    def __init__(self, from_currency, to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency

        Currency.url = f"https://api.transferwise.com/v1/rates?source={from_currency}&target={to_currency}"

    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
    def get_rate(self):
        """
        Output: Rate
        """
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url=Currency.url, headers=headers)
        print(response.json())

        return None


from_currency = "cad"
from_currency = from_currency.upper()

to_currency = "brl"
to_currency = to_currency.upper()


currency = Currency(from_currency, to_currency)

currency.get_rate()




class TransferWise:
    def __init__ (self, email, pwd, threshold):
        self.email = email
        self.pwd = pwd
        self.threshold = threshold

    
    def get_rate(self):
        headers = {}
        # url = https://api.sandbox.transferwise.tech/v1/rates?source=EUR&target=USD

    def get_threshold(self):
        return self.threshold
    
    def send_money(self):
        pass
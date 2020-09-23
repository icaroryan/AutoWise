import requests
from bs4 import BeautifulSoup

class Currency:

    url = None

    def __init__(self, from_currency, to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency

        Currency.url = f"https://www.investing.com/currencies/{from_currency}-{to_currency}".lower()

    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
    def get_rate(self):
        resp = requests.get(Currency.url)
        

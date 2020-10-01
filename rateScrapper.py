# https://api-docs.transferwise.com/#transferwise-api
# https://transferwise.com/help/articles/2958107/how-can-my-business-use-the-transferwise-api


import requests
from bs4 import BeautifulSoup
import lxml

class No_TransferWise:
    # Class Variables
    url = None

    def __init__(self, from_currency, to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency

        No_TransferWise.url = f"https://www.investing.com/currencies/{from_currency}-{to_currency}".lower()

    # Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
    def get_rate(self):
        """
        Output: Rate, Fluctuation
        """
        resp = requests.get(No_TransferWise.url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'lxml')
        div = soup.body.find("div", attrs={"class": "top bold inlineblock"})
        
        rate = div.select_one(".inlineblock.arial_26").get_text()
        # fluctuation = div.select_one(".parentheses.arial_20").get_text()

        return rate
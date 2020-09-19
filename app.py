import os, re
from time import sleep

# https://github.com/RomelTorres/alpha_vantage
from forex_python.converter import CurrencyRates

# Loading Environment Variables
from dotenv import load_dotenv
load_dotenv()

# Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
def get_exchange_rates(from_currency, to_currency):
    c = CurrencyRates()
    data = c.get_rate(from_currency, to_currency)
    print(f"{data}")
    sleep(2)


# Alphavantage API_KEY
try:
    api_key = os.environ.get('API_KEY')
except KeyError:
    print("API Key not found!")

# Prompt the user for the Currencies
from_currency = input(f"\nWhat Currency you want to convert FROM? (ex: USD) ")
to_currency = input(f"\nWhat Currency you want to convert TO? (ex: CAD) ")

# Ask if the user wants the automatic money sender turned ON (transfer wise)
auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach a threshold? ([Y]es or [N]o) ")
auto_mode = None
# auto_mode = re.??? ### TO-DO

while True:
    get_exchange_rates(from_currency, to_currency)

if auto_mode:
    pass
    # Prompt for the transferwise email
    # Prompt for the transferwise password (don't save this in a raw form, rather, encrypted way)
    


# INPUT: from_currency(str), to_currency(str)
# OUTPUT: rate (Float number, rounded by 4)

# Transfer
import os, re

# https://github.com/RomelTorres/alpha_vantage
from alpha_vantage.foreignexchange import ForeignExchange

# Loading Environment Variables
from dotenv import load_dotenv
load_dotenv()

# Alphavantage API_KEY
try:
    api = os.environ.get('API_KEY')
except KeyError:
    print("API Key not found!")

# Prompt the user for the Currencies
from_currency = input(f"\nWhat Currency you want to convert FROM? (ex: USD) ")
to_currency = input(f"\nWhat Currency you want to convert TO? (ex: CAD) ")

# Ask if the user wants the automatic money sender turned ON (transfer wise)
auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach a threshold? ([Y]es or [N]o) ")

auto_mode = None
# auto_mode = re.??? ### TO-DO

if auto_mode:
    pass
    # Prompt for the transferwise email
    # Prompt for the transferwise password (don't save this in a raw form, rather, encrypted way)
    

# Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
def get_exchange_rates(from_currency, to_currency):
    pass
# INPUT: from_currency(str), to_currency(str)
# OUTPUT: rate (Float number, rounded by 4)

# Transfer
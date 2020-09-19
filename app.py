import re, sys
from os import system, name 
from time import sleep
from datetime import datetime

# https://github.com/RomelTorres/alpha_vantage
from forex_python.converter import CurrencyRates, CurrencyCodes

cr = CurrencyRates()
cc = CurrencyCodes()

# Tracker (GET_EXCHANGE_RATES) -> Create a function that gets the chosen exchange rates
def get_exchange_rates(from_currency, to_currency, now):
    data = cr.get_rate(from_currency, to_currency, now)
    return data


def clear():
    # If windows
    if name == "nt":
        system('cls') 
    # If mac
    else:
        system('clear')

# Prompt the user for the Currencies
from_currency = input(f"\nWhat Currency you want to convert FROM? (ex: USD) ")

to_currency = input(f"What Currency you want to convert TO? (ex: CAD) ")

# Ask if the user wants the automatic money sender turned ON (transfer wise)
auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach a threshold? ([Y]es or [N]o) ")
auto_mode = None
# auto_mode = re.??? ### TO-DO
clear()
while True:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    now = datetime.now()

    try:
        rate = get_exchange_rates(from_currency, to_currency, now)
    except:
        print("\n Currency not found, please try again!")
        break

    print(f"\r1 {from_currency} = {round(rate, 4)} {to_currency}", end="")
    # print(f"1 {from_currency} = {round(rate, 4)} {to_currency}")
    sleep(1)

if auto_mode:
    pass
    # Prompt for the transferwise email
    # Prompt for the transferwise password (don't save this in a raw form, rather, encrypted way)
    


# INPUT: from_currency(str), to_currency(str)
# OUTPUT: rate (Float number, rounded by 4)

# Transfer
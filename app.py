import re, sys
from os import system, name 
from time import sleep
from datetime import datetime

from rateScrapper import *


# Clear the terminal
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



# Creating Currency
currency = Currency(from_currency, to_currency)

# Ask if the user wants the automatic money sender turned ON (transfer wise)
auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach a threshold? ([Y]es or [N]o) ")
auto_mode = None

# auto_mode = re.??? ### TO-DO
clear()

while True:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    rate = currency.get_rate()
    
    print(f"\r1 {from_currency} = {rate} {to_currency}", end="")
    # print(f"1 {from_currency} = {round(rate, 4)} {to_currency}")
    sleep(1)


    




# Transfer
if auto_mode:
    pass
    # Prompt for the transferwise email
    # Prompt for the transferwise password (don't save this in a raw form, rather, encrypted way)
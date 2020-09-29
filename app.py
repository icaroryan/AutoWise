import re, getpass
from os import system, name 
from time import sleep

from forex_python.converter import CurrencyCodes
c = CurrencyCodes()

# from rateScrapper import *
from transferwiseMode import *


# https://api-docs.transferwise.com/#transferwise-api
# https://transferwise.com/help/articles/2958107/how-can-my-business-use-the-transferwise-api

# Clear the terminal
def clear():
    # If windows
    if name == "nt":
        system('cls') 
    # If mac
    else:
        system('clear')

account = None

def auto_send():
    print(f"Activating TransferWise MODE\n")
    print(f"\nDon't worry, only you will have access to these information!\n")


    # Prompt for the transferwise email
    email = input("Your email address: ")
    # Prompt for the transferwise password (don't save this in a raw form, rather, encrypted way)
    pwd = getpass.getpass(prompt="Your password: ")
    while True:
        try:
            rate = currency.get_rate()[0]
            print(f"\nCurrent Exchange Rate: {from_currency} = {rate} {to_currency}")
            threshold = float(input(f"\nSend money when 1 {from_currency} moves bellow {c.get_symbol(to_currency)} "))
            break
        
        except ValueError:
            print("Invalid Value!")
            
    global account
    account = TransferWise(email, pwd, threshold)



# Prompt the user for the Currencies
from_currency = input(f"\nWhat Currency you want to convert FROM? (ex: USD) ")
from_currency = from_currency.upper()

to_currency = input(f"What Currency you want to convert TO? (ex: CAD) ")
to_currency = to_currency.upper()

# Creating Currency
currency = Currency(from_currency, to_currency)


while True:
    auto_mode = False

    # Ask if the user wants the automatic money sender turned ON (transfer wise)
    auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach your threshold? ([Y]es or [N]o) ")

    if auto_true := re.findall("^y$|^yes$", auto_prompt.lower()):
        clear()
        auto_send()
        auto_mode = True
        break

    elif auto_false := re.findall("^n$|^no$", auto_prompt.lower()):
        break

    else:
        print("Invalid answer! Please try again.")


clear()

print("EXCHANGE RATE TRACKER       TransferWise Mode: {auto_mode} {threshold}".format(auto_mode= auto_mode, threshold= f"(Threshold: {account.get_threshold()} {to_currency})" if account != None else ""))

while True:
    rate, fluctuation = currency.get_rate()
    
    print(f"\r1 {from_currency} = {rate} {to_currency}  ({fluctuation})", end="")
    # print(f"1 {from_currency} = {round(rate, 4)} {to_currency}")
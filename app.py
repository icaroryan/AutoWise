import re, getpass
from os import system, name 
from time import sleep
import sys

from forex_python.converter import CurrencyCodes
c = CurrencyCodes()

from rateScrapper import *
from transferwiseMode import *


# Clear the terminal
def clear():
    # If windows
    if name == "nt":
        system('cls') 
    # If mac
    else:
        system('clear')

currency = None

def auto_send():
    print(f"Activating TransferWise MODE...\n")
    print(f"\nDon't worry, only you will have access to these information!\n")


    # Prompt for the transferwise email
    # token = input("Your API Token: ")
    clear()

    global currency
    currency = TransferWise(from_currency, to_currency)

    while True:
        try:
            rate = currency.get_rate()
            print(f"Current Exchange Rate: {from_currency} = {rate} {to_currency}")
            threshold = float(input(f"\nSend money when 1 {from_currency} moves bellow {c.get_symbol(to_currency)} "))
            threshold = format(threshold, ".4f")
            break
        
        except ValueError:
            print("Invalid Value!")
            

    currency.set_threshold(threshold)



# Prompt the user for the Currencies
from_currency = input(f"\nWhat Currency you want to convert FROM? (ex: USD) ")
from_currency = from_currency.upper()

to_currency = input(f"What Currency you want to convert TO? (ex: CAD) ")
to_currency = to_currency.upper()

# Creating Currency


while True:
    auto_mode = False

    # Ask if the user wants the automatic money sender turned ON (transfer wise)
    auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach your threshold? ([Y]es / [N]o) ")

    if auto_true := re.findall("^y$|^yes$", auto_prompt.lower()):
        clear()
        auto_send()
        auto_mode = True
        break

    elif auto_false := re.findall("^n$|^no$", auto_prompt.lower()):
        currency = No_TransferWise(from_currency, to_currency)
        break

    else:
        print("Invalid answer! Please try again.")


clear()

threshold = currency.get_threshold()

print("EXCHANGE RATE TRACKER       TransferWise Mode: {auto_mode}    {threshold}".format(auto_mode= auto_mode, threshold= f"(Threshold: {threshold} {to_currency})       Refresh Rate: 1m" if auto_mode else "       Refresh Rate: 30s"))

threshold = float(threshold)


while True:
    rate = currency.get_rate()
    rate_f = float(rate)

    if rate_f <= threshold:
        print("Threshold reached!! Sending money...")
        input()

    if auto_mode:
        timer = 60
    else:
        timer = 30

    for i in range(timer):
        remaining = str(timer - i)
        sys.stdout.write(f"\r1 {from_currency} = {rate[:]} {to_currency}       {remaining.zfill(2)}s")
        sys.stdout.flush()
        sleep(1)
from transferwiseMode import *
import re
from os import system, name
from time import sleep
import sys


from forex_python.converter import CurrencyCodes
c = CurrencyCodes()

# from rateScrapper import *


# Clear the terminal
def clear():
    # If windows
    if name == "nt":
        system('cls')
    # If mac
    else:
        system('clear')


currency = None
current_recipient = None

clear()


print("============== Welcome to AutoWise ==============\n\n")




def auto_send():

    clear()
    while True:
        try:

            profile_id = currency.get_profile_id()
            currency.set_profile_id(profile_id)

            rate = currency.get_rate()
            print(
                f"Current Exchange Rate: 1 {to_currency} = \033[1;32;40m{rate} {from_currency}\033[0;37;40m")

            threshold = float(input(
                f"\nTransfer money when 1 {to_currency} drops below {c.get_symbol(from_currency)}"))

            amount = float(input(
                f"How much {from_currency} you want to send? (without commas, e.g. 12000) "))
            # targetAmount
            # sourceAmount

            currency.set_amount(amount)
            
            threshold = format(threshold, ".5f")
            currency.set_threshold(threshold)
            print(
                "\nWe have Upper and Lower Bounds to GUARANTEE that you get the best Exchange Rate possible.\nOnce a new threshold is reached, we create a new transfer and cancel your previous one to refresh it")

            recipients = currency.get_recipients()

            if len(recipients) < 1:
                print("You've got no recipient in your account. Add one and try again.")
                return False

            print(f"\n\n---Recipient Accounts---\n")
            for i, recipient in enumerate(recipients):
                print(f"{i + 1}: \033[1;34;40m{recipient['accountHolderName']} ({recipient['country']}/{recipient['currency']})\033[0;37;40m > Transit & Account Number: {recipient['details']['transitNumber']} - {recipient['details']['accountNumber']}  | Account Type: {recipient['details']['accountType']}")
            option = int(
                input(f"\nEnter the recipient you want to send money: "))
            recipient_target = option - 1
            currency.set_recipient(recipients[recipient_target])

            global current_recipient
            current_recipient = currency.get_recipient()

        except Exception as e:
            print(e)
            return False

        else:
            return True


from_currency = input(
    f"Source currency code (FROM)? (e.g. CAD) ")
from_currency = from_currency.upper()


# Prompt the user for the Currencies
to_currency = input(
    f"Target currency code (TO)? (e.g. USD) ")
to_currency = to_currency.upper()


# Creating Currency
currency = TransferWise(from_currency, to_currency)
auto_mode = auto_send()


clear()


print("AutoWise                                        Refresh Rate: 1m\n")
rate_index = 0

try:
    while True:
        # upper_threshold = currency.get_threshold()[0]
        user_threshold = currency.get_threshold()[1]
        # lower_threshold = currency.get_threshold()[2]

        current_threshold = currency.get_threshold()[rate_index]

        rate = currency.get_rate()
        rate_f = float(rate)

        if auto_mode and (round(rate_f, 4) <= current_threshold):
            threshold_type = ""
            if rate_index == 0:
                threshold_type = "Upper "
            elif rate_index == 1:
                threshold_type = " "
            elif rate_index == 2:
                threshold_type = "Lowest "
            else:
                threshold_type = "New lowest "

            print(
                f"\r{threshold_type}Threshold reached!! Sending money to {current_recipient['accountHolderName']}...")
            currency.send_money()

            if rate_index <= 2:
                rate_index += 1

        if rate_index > 2:
            current_threshold = round(current_threshold * 0.998, 5)

        timer = 60

        for i in range(timer):
            remaining = str(timer - i)
            sys.stdout.write("\r\033[1;32;40m1 {to_currency} = {rate} {from_currency}       \033[0;37;40m{remaining_seconds}s                {threshold} ".format(
                to_currency=to_currency, rate=rate, from_currency=from_currency, remaining_seconds=remaining.zfill(2), threshold=f"(Threshold: {user_threshold} {from_currency})"if auto_mode else ""))
            sys.stdout.flush()
            sleep(1)

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    input("\n\nPress enter to finish.")

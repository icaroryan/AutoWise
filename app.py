from transferwiseMode import *
import re
from os import system, name
from time import sleep
import sys
import beepy


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


def auto_send():

    print(f"Activating TransferWise MODE...\n")
    print(f"\nDon't worry, only you will have access to these information!\n")

    # Prompt for the transferwise email
    # token = input("Your API Token: ")
    clear()

    while True:
        try:

            profile_id = currency.get_profile_id()
            currency.set_profile_id(profile_id)

            rate = currency.get_rate()
            print(
                f"Current Exchange Rate: 1 {to_currency} = \033[1;32;40m{rate} {from_currency}\033[0;37;40m")

            amount = float(input(
                f"How much {from_currency} you want to send? (without commas, ex. 12000) "))
            # targetAmount
            # sourceAmount

            currency.set_amount(amount)

            threshold = float(input(
                f"\nSend money when 1 {to_currency} moves bellow {c.get_symbol(from_currency)} "))
            threshold = format(threshold, ".4f")
            currency.set_threshold(threshold)
            print(
                "We have Upper and Lower Bounds to GUARANTEE that you get the best Exchange Rate possible.\nOnce a new threshold is reached, we create a new transfer and cancell your previous one to refresh it")

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


# Prompt the user for the Currencies
to_currency = input(
    f"\nWhat Currency you want to convert FROM [Target(receive) currency code]? (ex: USD) ")
to_currency = to_currency.upper()

from_currency = input(
    f"What Currency you want to convert TO [Source(send) currency code]? (ex: CAD) ")
from_currency = from_currency.upper()

# Creating Currency


while True:
    auto_mode = False

    # Ask if the user wants the automatic money sender turned ON (transfer wise)
    auto_prompt = input(
        f"\nDo you want us to automatically open a transaction when the Exchange Rate reach your threshold? ([Y]es / [N]o) ")

    currency = TransferWise(from_currency, to_currency)

    if auto_true := re.findall("^y$|^yes$", auto_prompt.lower()):
        clear()
        auto_mode = auto_send()
        break

    elif auto_false := re.findall("^n$|^no$", auto_prompt.lower()):
        break

    else:
        print("Invalid answer! Please try again.")


clear()


print("EXCHANGE RATE TRACKER       TransferWise Mode: {}       Refresh Rate: 1m\n".format(auto_mode))
rate_index = 0

try:
    while True:
        # upper_threshold = currency.get_threshold()[0]
        user_threshold = currency.get_threshold()[1]
        # lower_threshold = currency.get_threshold()[2]
        if rate_index <= 2:
            current_threshold = currency.get_threshold()[rate_index]

        rate = currency.get_rate()
        rate_f = float(rate)

        if auto_mode and (rate_f <= current_threshold):
            if rate_index == 0:
                threshold_type = "Upper "
            elif rate_index == 1:
                threshold_type = ""
            elif rate_index == 2:
                threshold_type = "Lower "
            else:
                threshold_type = "Even lower "

            print(
                f"\r{threshold_type}Threshold reached!! Sending money to {current_recipient['accountHolderName']}...")
            currency.send_money()
            beepy.beep(sound='ping')
            rate_index += 1

        if rate_index > 2:
            current_threshold = round(current_threshold * 0.998, 4)

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
    input("\n\nCongratulations!!! You got the best rate as possible on TransferWise! Press enter to finish.")

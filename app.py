import re
from os import system, name 
from time import sleep
import sys


from forex_python.converter import CurrencyCodes
c = CurrencyCodes()

# from rateScrapper import *
from transferwiseMode import *

def beep():
    duration = 250  # milliseconds
    freq = 700  # Hz
    for i in range(2):
        if name == "nt":
            import winsound
            winsound.Beep(freq, duration)
        # If mac
        else:
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    
        
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


    while True:
        try:

            profile_id = currency.get_profile_id()
            currency.set_profile_id(profile_id)

            rate = currency.get_rate()
            print(f"Current Exchange Rate: 1 {to_currency} = {rate} {from_currency}")

            amount = float(input(f"How much {from_currency} you want to send? (without commas, ex. 12000) "))
            # targetAmount
            # sourceAmount

            currency.set_amount(amount)
            
            threshold = float(input(f"\nSend money when 1 {to_currency} moves bellow {c.get_symbol(from_currency)} "))
            threshold = format(threshold, ".4f")
            currency.set_threshold(threshold)


            recipients = currency.get_recipients()    

            if len(recipients) < 1:
                print("You've got no recipient in your account. Add one and try again.")
                return False

            print(f"\n\n---Recipient Accounts---\n")
            for i, recipient in enumerate(recipients):
                print(f"{i + 1}: {recipient['accountHolderName']} ({recipient['country']}/{recipient['currency']}) > Transit & Account Number: {recipient['details']['transitNumber']} - {recipient['details']['accountNumber']}  | Account Type: {recipient['details']['accountType']}")
            option = int(input(f"\nEnter the recipient you want to send money: "))
            recipient_target = option - 1
            currency.set_recipient(recipients[recipient_target])
        
        except Exception as e:
            print(e)
            return False
        
        else:
            return True
        
    


# Prompt the user for the Currencies
to_currency = input(f"\nWhat Currency you want to convert FROM [Target(receive) currency code]? (ex: USD) ")
to_currency = to_currency.upper()

from_currency = input(f"What Currency you want to convert TO [Source(send) currency code]? (ex: CAD) ")
from_currency = from_currency.upper()

# Creating Currency


while True:
    auto_mode = False

    # Ask if the user wants the automatic money sender turned ON (transfer wise)
    auto_prompt = input(f"\nDo you want us to automatically open a transaction when the Exchange Rate reach your threshold? ([Y]es / [N]o) ")

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

if auto_mode:
    threshold = currency.get_threshold()

print("EXCHANGE RATE TRACKER       TransferWise Mode: {auto_mode}    {threshold}       Refresh Rate: 1m".format(auto_mode= auto_mode, threshold= f"(Threshold: {threshold} {from_currency})"if auto_mode else ""))

if auto_mode:
    threshold = float(threshold)


while True:
    rate = currency.get_rate()
    rate_f = float(rate)


    if auto_mode and (rate_f <= threshold):
        print("\rThreshold reached!! Sending money...")
        currency.send_money()
        break

    timer = 60

    for i in range(timer):
        remaining = str(timer - i)
        sys.stdout.write(f"\r1 {to_currency} = {rate} {from_currency}       {remaining.zfill(2)}s")
        sys.stdout.flush()
        sleep(1)


input("Press ENTER to exit")
    
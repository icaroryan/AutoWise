import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import sys
from forex_python.converter import CurrencyCodes

from TransferWise import TransferWise


class AutoWise:
    def __init__(self):
        self.last_transfer = {}
        self.last_idle_transfer = {}
        self.thresholds = []


    def set_currencies(self, source_currency, target_currency):
        self.source_currency = source_currency
        self.target_currency = target_currency
    

    def set_amount(self, amount):
        self.amount = amount


    def set_recipient(self):
        tw = TransferWise()

        recipients = tw.get_recipients(self.target_currency)

        if len(recipients) < 1:
            print("You've got no recipient in your account. Add one and try again.")
            return False

        print(f"\n\n---Recipient Accounts---\n")
        for i, recipient in enumerate(recipients):
            print(f"{i + 1}: \033[1;34;40m{recipient['accountHolderName']} ({recipient['country']}/{recipient['currency']})\033[0;37;40m > Transit & Account Number: {recipient['details']['transitNumber']} - {recipient['details']['accountNumber']}  | Account Type: {recipient['details']['accountType']}")
        option = int(
            input(f"\nEnter the recipient you want to send money: "))

        recipient_target = option - 1

        self.recipient = recipients[recipient_target]
        

    def set_profile_id(self):
        self.profile_id = self.get_profile_id()


    def set_threshold(self, threshold):
        threshold = float(threshold)
        # 0.3% more
        upper_bound = round(threshold * 1.002, 5)
        # 0.3% less
        lower_bound = round(threshold * 0.998, 5)
        self.thresholds.extend([upper_bound, threshold, lower_bound])


    def get_source_currency(self):
        return self.source_currency


    def get_target_currency(self):
        return self.target_currency


    def get_amount(self):
        return self.amount


    def get_recipient(self):
        return self.recipient

    def get_recipients(self):
        tw = TransferWise()
        return tw.get_recipients(self.target_currency)


    def get_profile_id(self):
        tw = TransferWise()
        response =  tw.get_profile_id()

        profile_n = 0
        if len(response) > 1:
            print("-- Profiles --")
            for i, profile in enumerate(response):
                try:
                    print(
                        f"{i + 1}: \033[1;34;40m{profile['details']['firstName']} {profile['details']['lastName']}\033[0;37;48m > Type: {profile['type']} (ID: {profile['id']})")
                except KeyError:
                    print(
                        f"{i + 1}: \033[1;34;40m{profile['details']['name']}\033[0;37;48m > Type: {profile['type']} (ID: {profile['id']})")

            option = int(input(
                "\nWe noticed you have more than one profile in your account. \nEnter the profile number you want to send money from: "))
            print()
            profile_n = option - 1

        return response[profile_n]["id"]


    def get_threshold(self):
        return self.thresholds

    
    def quote_rate(self, source_currency, target_currency):
        url = f"https://transferwise.com/gb/currency-converter/{target_currency}-to-{source_currency}-rate"

        while True:
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(resp.text, 'html.parser')
            span = soup.body.find("span", attrs={"class": "text-success"})

            # rate = div.select_one(".inlineblock.arial_26").get_text()
            try:
                rate = float(span.get_text())
            # Make sure the page is returning a value
            except AttributeError:
                continue
            else:
                break
            # fluctuation = div.select_one(".parentheses.arial_20").get_text()

        rate = round(rate, 5)
        return rate



    def quote(self):
        tw = TransferWise()
        response = tw.quote(self.source_currency, self.target_currency, self.profile_id, self.amount)

        if self.last_transfer:
            self.last_idle_transfer = self.last_transfer.copy()

        self.quote_id = response['id']

        self.sourceAmount = response['sourceAmount']
        targetAmount = response['targetAmount']
        fee = response['fee']

        commercial_rate = format(
            (self.sourceAmount - fee) / targetAmount, '.5f')
        self.last_transfer["rate"] = commercial_rate

        vet = format(self.sourceAmount / targetAmount, '.5f')

        createdTime = response['createdTime']
        objDate = datetime.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        createdTime = objDate.strftime("%B %d, %Y %H:%M:%S")

        print(f"\nYou send {self.sourceAmount} {self.source_currency} >> Recipient gets {targetAmount} {self.target_currency} \nCommercial rate: {commercial_rate}   ||   That's 1 {self.target_currency} = {vet} {self.source_currency} Effective Rate (VET)")

    
    def create_transfer(self):
        tw = TransferWise()
        response = tw.create_transfer(self.recipient, self.quote_id)


        self.last_transfer["id"] = response["id"]
        self.last_transfer["rate"] = response["rate"]

        created_date = response["created"]
        rate = response["rate"]
        source_value = response["sourceValue"]
        source_Currency = response["sourceCurrency"]

        target_value = round(source_value * rate, 2)
        target_Currency = response["targetCurrency"]

        print(
            f"\nTransfer created successfully! \033[1;32;40m{target_value} {target_Currency}   \033[0;37;40m({self.sourceAmount} {source_Currency})     [{created_date}]")

        if self.last_idle_transfer:
            self.cancel_transfer()

        print("----------------------------------------------------------------------------------------------\n")

    
    def cancel_transfer(self):
        # transfer_id = self.last_transfer["id"]
        transfer_id = self.last_idle_transfer["id"]
        current_transfer_rate = self.last_transfer["rate"]
        transfer_rate = self.last_idle_transfer["rate"]

        print(
            f"\nNice, You got an even better rate! We're keeping the best one.")

        tw = TransferWise()
        response = tw.cancel_transfer(transfer_id)

        print(
                f"Exchange rate decreased from {transfer_rate} to {current_transfer_rate}!")


    def send_money(self):
        self.quote()
        self.create_transfer()


    def setup(self):
        tw = TransferWise()

        self.set_profile_id()

        rate = self.quote_rate(self.source_currency, self.target_currency)
        print(
            f"Current Exchange Rate: 1 {self.target_currency} = \033[1;32;40m{rate} {self.source_currency}\033[0;37;40m")


        c = CurrencyCodes()
        threshold = float(input(
            f"\nTransfer money when 1 {self.target_currency} drops below {c.get_symbol(self.source_currency)} "))

        self.set_threshold(format(threshold, ".5f"))            


        amount = float(input(
            f"How much {self.source_currency} you want to send? (without commas, e.g. 12000) "))

        self.set_amount(amount)
        
        
        print(
            "\nWe have Upper and Lower Bounds to GUARANTEE that you get the best Exchange Rate possible.\nOnce a new threshold is reached, we create a new transfer and cancel your previous one to refresh it")
        
        self.set_recipient()

    

    def start(self):
        print("AutoWise                                        Refresh Rate: 1m\n")
        rate_index = 0
        
        while True:
            # upper_threshold = currency.get_threshold()[0]
            user_threshold = self.get_threshold()[1]
            # lower_threshold = currency.get_threshold()[2]

            current_threshold = self.get_threshold()[rate_index]

            rate = self.quote_rate(self.source_currency, self.target_currency)
            rate_f = float(rate)

            if round(rate_f, 4) <= current_threshold:
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
                    f"\r{threshold_type}Threshold reached!! Sending money to {self.recipient['accountHolderName']}...")
                self.send_money()

                if rate_index <= 2:
                    rate_index += 1

            if rate_index > 2:
                current_threshold = round(current_threshold * 0.998, 5)

            timer = 60

            for i in range(timer):
                remaining = str(timer - i)
                sys.stdout.write("\r\033[1;32;40m1 {target_currency} = {rate} {source_currency}       \033[0;37;40m{remaining_seconds}s                {threshold} ".format(
                    target_currency=self.target_currency, rate=rate, source_currency=self.source_currency, remaining_seconds=remaining.zfill(2), threshold=f"(Threshold: {user_threshold} {self.source_currency})"))
                sys.stdout.flush()
                sleep(1)

        
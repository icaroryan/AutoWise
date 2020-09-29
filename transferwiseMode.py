# https://api-docs.transferwise.com/#transferwise-api
# https://transferwise.com/help/articles/2958107/how-can-my-business-use-the-transferwise-api

from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")

class TransferWise:
    def __init__ (self, email, pwd, threshold):
        self.email = email
        self.pwd = pwd
        self.threshold = threshold

    
    def get_threshold(self):
        return self.threshold
    
    def send_money(self):
        pass
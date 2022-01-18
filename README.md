# AutoWise

A Python script to help you save money when sending money internationally. This script uses BeautifulSoup to track the fluctuations in conversion rates between currencies and find the lowest exchange rate to send money from one country to another.

Upon the desired rate is reached, the script will utilize REST Api to perform an API request to create a transaction on TransferWise, a platform to send and receive money from overseas. Upon a new lowest exchange rate, this application will perform a new request to the API to update the transaction. Say goodbye to the hassle of timing the market to get the best conversion rate between two currencies, AutoWise does it for you!

## 🛠 Tech Stack
| <img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png" width="40"> |
- **Languages Used**: Python, RESTful API, BeautifulSoup </br>

## ⚙️ Features

- Simple and easy user interface.
- Track the exchange rate between two currencies.
- Allow the user to choose the amount to send and the desired exchange rate.
- Select the recipient account to receive the transfer.
- Open an automatic transfer on Wise (ex TransferWise) to send money internationally when the best rate is reached.

## 🔧 Setup

1. Login into your TransferWise (aka Wise)
2. Open the account settings

![image](https://user-images.githubusercontent.com/50868010/149875919-9ee150b9-03fd-47c9-82c5-e69698d8f7a9.png)

3. Scroll down and untoggle the "API Tokens" option
4. Click on "Add new Token"

![image](https://user-images.githubusercontent.com/50868010/149876164-8e237f2c-c567-4ae9-87fc-e664bc5984f4.png)

5. Give it a nice name and hit "Full Access"
6. "Create Token"

![image](https://user-images.githubusercontent.com/50868010/149876602-61670a7e-b5dd-4c31-bc2a-5aaa39a9a9ac.png)

7. Go back to "API Tokens" and copy your key

![image](https://user-images.githubusercontent.com/50868010/149876803-fff22c58-bbe4-46ab-97b5-7fca464d8294.png)

8. Inside the AutoWise folder, you'll find a file called ".env.example". Open it and append your key after "API_TOKEN=" <br/>
e.g. API_TOKEN=6abcdac4-7d4c-4c45-bbf8-aeebc628d3ed
10. Save the file and rename it to ".env"

![2022-01-18_00-38-37_AdobeCreativeCloudExpress (1)](https://user-images.githubusercontent.com/50868010/149877643-e0974ccf-5588-4c88-b1b7-13ec25960e93.gif)



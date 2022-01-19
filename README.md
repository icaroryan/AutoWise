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

## 💎 Usage
```sh
python app.py
```

## 👀 Application Preview

### Don't time the market. Let us do it for you! 📉

## **1. Selecting currencies**
In this screen, the user will select the currencies that they want to sent money from/to.
![image](https://user-images.githubusercontent.com/50868010/150044547-75736051-0fb8-493a-ad35-7e5d996077d2.png)



## **2. Selecting target rate, amount and recipient account**
After selecting the currencies, the user will be able to choose his target exchange rate, amount , and one of recipient added in his account. <br />

![image](https://user-images.githubusercontent.com/50868010/150044667-21de3ec8-e923-4889-860e-3776d0409ab6.png)


## **3. Tracking the Forex Market 📈**
The software will take into consideration the user target rate and will place a transfer when the exchange rate between the two currencies chosen before is less or equals the target rate.

![image](https://user-images.githubusercontent.com/50868010/150044761-0fb4d27b-59f7-421e-9a51-c92d22c4b923.png)

As you can see in the picture below, we started on a high market, which isn't what we want.

![wise11](https://user-images.githubusercontent.com/50868010/150047318-d78aeb30-e12e-4816-af42-49be9b313d31.jpg)


## **4. Buying the DIP 📉**
When the script find the best moment to create a transfer, it'll do it for you automatically. Therefore, you don't need to keep watching all those graphs 24/7.


![image](https://user-images.githubusercontent.com/50868010/150045266-b4d3b095-bb57-475a-9bc0-07391c5036e5.png)

![wise7](https://user-images.githubusercontent.com/50868010/150047249-311a3ec0-ee4f-4acc-a775-e662b95fc351.jpg)


## **5. Buying the DIP (again) 📉**
The best part of it is that it'll keep getting the lowest Exchange Rate as long as the script is in execution. <br/ >
Not only did AutoWise manage to reach the target rate, but it went above and beyond by finding an even better exchange rate.

![image](https://user-images.githubusercontent.com/50868010/150046502-dca4ded2-fade-48eb-b17a-80397a94340d.png)

![wise10](https://user-images.githubusercontent.com/50868010/150047331-e761782b-34c7-4a6f-959a-2726f633590e.jpg)


*Rate progression in a couple of hours: *

## **6. Rate guaranteed on Wise 💲**
After finding the best conversion rate, your transfer will be secured on Wise.

![image](https://user-images.githubusercontent.com/50868010/150047173-c9a4c00e-2664-419a-b52e-7d4d0036516f.png)




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



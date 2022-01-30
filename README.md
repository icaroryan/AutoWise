# AutoWise

A Python script to help you save money when sending money internationally. This script uses BeautifulSoup to track the fluctuations in conversion rates between currencies and find the lowest exchange rate to send money from one country to another.

Once the desired rate is reached, the script will utilize REST Api to perform an API request to create a transaction on TransferWise, a platform to send and receive money from overseas. Upon detecting a lower exchange rate than the current transaction, this application will perform a new request to the API to update the transfer. Say goodbye to the hassle of timing the market to get the best conversion rate between two currencies. AutoWise will do it for you!

Table of contents
=================

<!--ts-->
   * [Tech Stack](#-tech-stack)
   * [Features](#%EF%B8%8F-features)
   * [Usage](#-usage)
   * [Application Demo](#-application-demo)
   * [Environment Variables](#-environment-variables)
   * [Setup](#-setup)

<!--te-->
## 🛠 Tech Stack

| <img width="40px" height="40px" src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"/> |
- **Languages Used**: Python, RESTful API, BeautifulSoup </br>

## ⚙️ Features

- Simple and easy user interface.
- Track the exchange rate between two currencies.
- Allow the user to choose the amount to send and the desired exchange rate.
- Select the recipient account to receive the transfer.
- Open an automatic transfer on Wise (ex TransferWise) to send money internationally when the best rate is reached.

## 💎 Usage
1. Clone repository with ```git clone https://github.com/icaroryan/AutoWise.git```
2. Follow [setup](#-setup) instructions
3. Open Command line in the application folder
4. Install all needed packages by running the command  ```pip install -r requirements.txt ```
4. Run app with command ```python app.py ```
5. Select currencies to send money from/to
6. Select the target rate, amount and recipient account
7. Relax, and let us do the hard work

## 👀 Application Demo

### Don't time the market. Let us do it for you! 📉

### **1. Selecting currencies**
In this screen, the user will select the currencies that they want to sent money from/to.
![image](https://user-images.githubusercontent.com/50868010/150044547-75736051-0fb8-493a-ad35-7e5d996077d2.png)



### **2. Selecting target rate, amount and recipient account**
After selecting the currencies, the user will be able to choose their target exchange rate, amount to be sent, and a recipient from their recipient list. <br />

![image](https://user-images.githubusercontent.com/50868010/150044667-21de3ec8-e923-4889-860e-3776d0409ab6.png)


### **3. Tracking the Forex Market 📈**
The software will take into consideration the user's target rate, and will place a transfer when the exchange rate of their selected currencies reaches below, or is at least equal to, the user's desired rate.

![image](https://user-images.githubusercontent.com/50868010/150044761-0fb4d27b-59f7-421e-9a51-c92d22c4b923.png)

As you can see in the picture below, we started on a high market, which isn't what we want.

![wise11](https://user-images.githubusercontent.com/50868010/150047318-d78aeb30-e12e-4816-af42-49be9b313d31.jpg)


### **4. Buying the DIP 📉**
When the script finds the best moment to create a transfer, it will do so automatically, thus, eliminating the need for the user to watch the graphs 24/7.


![image](https://user-images.githubusercontent.com/50868010/150045266-b4d3b095-bb57-475a-9bc0-07391c5036e5.png)

![wise7](https://user-images.githubusercontent.com/50868010/150047249-311a3ec0-ee4f-4acc-a775-e662b95fc351.jpg)


### **5. Buying the DIP (again) 📉**
The best part of it is that it'll keep getting the lowest Exchange Rate as long as the script is in execution. <br/ >
This is evident in the images below; not only did AutoWise manage to reach the target rate, but it went above and beyond by finding an even better exchange rate.

![image](https://user-images.githubusercontent.com/50868010/150046502-dca4ded2-fade-48eb-b17a-80397a94340d.png)

![wise10](https://user-images.githubusercontent.com/50868010/150047331-e761782b-34c7-4a6f-959a-2726f633590e.jpg)


**Results progression in only a couple of hours: 0.22677 > 022559 > 0.22503**

### **6. Rate guaranteed on Wise 💲**
After finding the best conversion rate, your transfer will be secured on Wise.

![image](https://user-images.githubusercontent.com/50868010/150047173-c9a4c00e-2664-419a-b52e-7d4d0036516f.png)


## 🔑 Environment Variables
To run the application, the following environment variable must be added: <br/> <br/>
```API_TOKEN```

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
e.g. ```API_TOKEN=6abcdac4-7d4c-4c45-bbf8-aeebc628d3ed```
10. Save the file and rename it to ".env"

![2022-01-18_00-38-37_AdobeCreativeCloudExpress (1)](https://user-images.githubusercontent.com/50868010/149877643-e0974ccf-5588-4c88-b1b7-13ec25960e93.gif)



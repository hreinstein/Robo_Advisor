# app/robo.py

import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv()
import datetime


#format to usd
def to_usd(my_price):
    return "${0:.2f}".format(my_price) #> $10,000.00

# Ino inputs

print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") 
symbol = "TSLA" # todo: ask for user input 

# request API url 
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
print(type(response)) #> <class 'requests.models.Response'>
print(response.status_code) #> 200
#print(type(response.text)) #> str, need to parse this to make into a dictionary below 

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict 
print(parsed_response)


# compute lastest day 
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


# compute latest close
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) # TODO: assumes the first day in on top, sort to ensure that the latest day is first 
latest_day = dates[0] #"2020-02-19"
latest_close = tsd[latest_day]["4. close"] #> 1,000.00


# maximum of all high prices
high_prices = []
low_prices = []


for date in dates: 
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#handle response errors: 
if "Error Messge" in response.text:
    print("Sorry, could not find that symbol, please try again")
    exit() 

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") #TODO: use date time module
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}") # maximum of all daily high prices
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


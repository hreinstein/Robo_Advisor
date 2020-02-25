# app/robo.py

import requests
import json
import csv
import os 
from dotenv import load_dotenv
import datetime

load_dotenv() 

# format to usd
def to_usd(my_price):
    return "${0:.2f}".format(my_price) #> $10,000.00


# Inputs

#API Key 

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") 
symbol = input("Please enter a company ticker: ") 

# preliminary validation 
if str.isnumeric(symbol) or len(symbol) > 5: 
    print("Sorry, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
    symbol = input("Please enter a company ticker: ") 


# request API url 
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("Requesting some Data from the internet...")
print("Request URL:", request_url)
print("\n")

response = requests.get(request_url)

# response errors validation
if "Error Message" in response.text:
    print(f"Sorry, could not find {symbol}, please enter a valid ticker.")
    exit() 
else: 
    parsed_response = json.loads(response.text) 

# compute lastest day / last refreshed 
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) # TODO: assumes the first day is on top, sort to ensure that the latest day is first 
latest_day = dates[0] #"2020-02-19"

# compute lastest close 
latest_close = tsd[latest_day]["4. close"] #> 1,000.00

# compute high and low prices 
high_prices = []
low_prices = []

for date in dates: 
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)


# csv 
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

#date and time 
today = datetime.datetime.today()

#-------------------------------------------------------------------------------------------------------------------

# outputs 


print("-------------------------")
print(f"SELECTED STOCK: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", today.strftime("%m/%d/%Y %I:%M %p")) 
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}") # maximum of all daily high prices
print(f"RECENT LOW: {to_usd(float(recent_low))}") # minimum ""
print("-------------------------")                    
if float(latest_close) <= (float(recent_low) * 1.15) and float(latest_close) < (float(recent_high) + float(recent_low))/2:
    print("RECOMMENDATION: BUY!")
    print(f"RECOMMENDATION REASON: {symbol}'s latest closing price is less than 15% above its recent low and less than {symbol}'s average price, satisfying the 'BUY' threshold.") 
elif float(latest_close) >= (float(recent_high) * .85) and float(latest_close) > (float(recent_high) + float(recent_low))/2:
     print("RECOMMENDATION: Sell!")
     print(f"RECOMMENDATION REASON: {symbol}'s latest closing price is greater than 85% of its recent high and greater than {symbol}'s average price, satisfying the 'SELL' threshold.") 
else: 
    print("RECOMMENDATION: HOLD")
    print(f"RECOMMENDATION REASON: {symbol}'s stock performance is steady, we recommend to HOLD for now.") 
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path} ...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


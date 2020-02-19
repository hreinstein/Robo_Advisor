# app/robo.py

import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") 

symbol = "TSLA" # todo: ask for user input 

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
print(type(response)) #> <class 'requests.models.Response'>
print(response.status_code) #> 200
#print(type(response.text)) #> str, need to parse this to make into a dictionary below 

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict 
print(parsed_response)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


#handle response errors: 
if "Error Messge" in response.text:
    print("Sorry, could not find that symbol, please try again")
    exit() 

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


# app/robo.py
import json
import csv
import os 
import datetime

from dotenv import load_dotenv
import requests


load_dotenv() 

# API Key 
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") 
symbol = input("Please enter a company ticker: ") 


# format to usd
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes. 
    
    Param: my_price (int or float) like 20.2222

    Example: to usd(20.2222)
    Returns: $20.22
    """
    return "${0:.2f}".format(my_price) #> $10,000.00

def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    print("Requesting some Data from the internet...")
    print("Request URL:", request_url)
    print("\n")
    response = requests.get(request_url)

    if "Error Message" in response.text:
        print(f"Sorry, could not find stock symbol {symbol}, please enter a valid company ticker.")
        exit() 
    else: 
        parsed_response = json.loads(response.text) 

    parsed_response = json.loads(response.text)
    return parsed_response


def transform_response(parsed_response):
    """
    parsed_response should be a dictionary representing the original JSON response
    it should have keys: "Meta Data" and "Time Series Daily
    """
    tsd = parsed_response["Time Series (Daily)"]
    
    dates = list(tsd.keys()) # TODO: assumes the first day is on top, sort to ensure that the latest day is first 
    #latest_day = dates[0] #"2020-02-19"

    rows = []
    for date, daily_prices in tsd.items(): # see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        rows.append(row)

    return rows


def write_to_csv(rows, csv_filepath):
    """
    rows should be a list of dictionaries
    csv_filepath should be a string filepath pointing to where the data should be written
    """
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)
    return True 



if __name__ == "__main__":

    today = datetime.datetime.today()  # date and time 

    parsed_response = get_response(symbol)

    while True:
        if str.isnumeric(symbol) or len(symbol) > 5: 
            print("Sorry, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
            symbol = input("Please enter a company ticker: ") 
        else:
            break

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    rows = transform_response(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes
    recent_high = max(high_prices)
    recent_low = min(low_prices)

    # NEW OUTPUTS 

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    write_to_csv(rows, csv_file_path)

    # PRINT RESULTS 

    formatted_time_now = today.strftime("%Y-%m-%d %H:%M:%S") #> '2019-03-03 14:45:27'

    #formatted_csv_file_path = csv_file_path.split("../")[1] #> data/prices.c
    
    print("-------------------------")
    print(f"SELECTED STOCK: {symbol}")
    print("-------------------------")
    print(f"REQUEST AT: {formatted_time_now}") 
    print(f"LATEST DAY: {last_refreshed}")
    print("-------------------------")
    print(f"LATEST CLOSE: {to_usd(latest_close)}")
    print(f"RECENT HIGH:  {to_usd(recent_high)}") # maximum of all daily high prices
    print(f"RECENT LOW:   {to_usd(recent_low)}") # minimum ""
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







# -------------------------------------------------------------------------------------------------------------------------


# request API url 
#request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
#print("Requesting some Data from the internet...")
#print("Request URL:", request_url)
#print("\n")
#
#response = requests.get(request_url)
#
## response errors validation
#if "Error Message" in response.text:
#    print(f"Sorry, could not find stock symbol {symbol}, please enter a valid company ticker.")
#    exit() 
#else: 
#    parsed_response = json.loads(response.text) 
#
## compute lastest day / last refreshed 
#last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
#
##tsd = parsed_response["Time Series (Daily)"]
#dates = list(tsd.keys()) # TODO: assumes the first day is on top, sort to ensure that the latest day is first 
#latest_day = dates[0] #"2020-02-19"





# compute lastest close 
#latest_close = tsd[latest_day]["4. close"] #> 1,000.00

# compute high and low prices 
#high_prices = []
#low_prices = []
#
#for date in dates: 
#    high_price = tsd[date]["2. high"]
#    low_price = tsd[date]["3. low"]
#    high_prices.append(float(high_price))
#    low_prices.append(float(low_price))
#
#recent_high = max(high_prices)
#recent_low = min(low_prices)


# csv 
#csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
#
#csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
#with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
#    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
#    writer.writeheader() # uses fieldnames set above
#    for date in dates:
#        daily_prices = tsd[date]
#        writer.writerow({
#            "timestamp": date,
#            "open": daily_prices["1. open"],
#            "high": daily_prices["2. high"],
#            "low": daily_prices["3. low"],
#            "close": daily_prices["4. close"],
#            "volume": daily_prices["5. volume"]
#        })
#


#-------------------------------------------------------------------------------------------------------------------

# outputs 


#print("-------------------------")
#print(f"SELECTED STOCK: {symbol}")
#print("-------------------------")
#print(f"REQUEST AT: {formatted_time_now}") 
#print(f"LATEST DAY: {last_refreshed}")
#print("-------------------------")
#print(f"LATEST CLOSE: {to_usd(latest_close)}")
#print(f"RECENT HIGH:  {to_usd(recent_high)}") # maximum of all daily high prices
#print(f"RECENT LOW:   {to_usd(recent_low)}") # minimum ""
#print("-------------------------")                    
#if float(latest_close) <= (float(recent_low) * 1.15) and float(latest_close) < (float(recent_high) + float(recent_low))/2:
#    print("RECOMMENDATION: BUY!")
#    print(f"RECOMMENDATION REASON: {symbol}'s latest closing price is less than 15% above its recent low and less than {symbol}'s average price, satisfying the 'BUY' threshold.") 
#elif float(latest_close) >= (float(recent_high) * .85) and float(latest_close) > (float(recent_high) + float(recent_low))/2:
#     print("RECOMMENDATION: Sell!")
#     print(f"RECOMMENDATION REASON: {symbol}'s latest closing price is greater than 85% of its recent high and greater than {symbol}'s average price, satisfying the 'SELL' threshold.") 
#else: 
#    print("RECOMMENDATION: HOLD")
#    print(f"RECOMMENDATION REASON: {symbol}'s stock performance is steady, we recommend to HOLD for now.") 
#print("-------------------------")
#print(f"WRITING DATA TO CSV: {csv_file_path} ...")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")



    # INFO INPUTS 
    #

    # preliminary validation 
    #while True:
    #    if str.isnumeric(symbol) or len(symbol) > 5: 
    #        print("Sorry, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
    #        symbol = input("Please enter a company ticker: ") 
    #    else:
    #        break


    # response errors validation

    #response = requests.get(request_url)

    #if "Error Message" in response.text:
    #    print(f"Sorry, could not find stock symbol {symbol}, please enter a valid company ticker.")
    #    exit() 
    #else: 
    #    parsed_response = json.loads(response.text) 
#
    # compute lastest day / last refreshed 
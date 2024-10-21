import re
import pandas
from stocks_operations import stock_real_time_values, stock_historical_values
import asyncio  # Import asyncio for async execution
import datetime
import yfinance
from datetime import timedelta
from variables import index_timezone, my_stocks_list_data
import pytz

# Function to search for keys using regex with case insensitivity
def search_dict_regex(d, pattern):
    # Using re.IGNORECASE for case-insensitive search
    matching_keys = [key for key in d.keys() if re.search(pattern, key, re.IGNORECASE)]
    return matching_keys

# Convert html data into a pandas dataframe
def html_data_into_dataframe(url):
    table = pandas.read_html(url)
    # in 0 we will find our index table
    return pandas.DataFrame(table[0])

# Convert pandas Dataframe into a dictionary
def dataframe_into_dict(dataframe):
    data_as_list = dataframe.values.tolist()

    my_dict = {}
    dataframe_lenght = len(data_as_list)
    counter = 0
    while dataframe_lenght > counter:
        my_dict[data_as_list[counter][1]] = data_as_list[counter][0]
        counter += 1
    return my_dict

# Check stocks values for a stock list
def stocks_values(array, operation, period = '1mo', show_plot = False):
    array_lenght = len(array)
    counter = 0
    stock_general_data = []

    while array_lenght > counter:
        stock_data = {}
        if(operation == 'historical'):
            stock_data["stock_ticker"] = array[counter]
            stock_data["stock_historical_data"] = stock_historical_values(array[counter], period, show_plot)
        elif(operation == 'real_time'):
            stock_data["stock_ticker"] = array[counter]
            stock_data["stock_real_time_data"] = str(stock_real_time_values(array[counter]))
        elif(operation == 'historical_and_real_time'):
            stock_data["stock_ticker"] = array[counter]
            stock_data["stock_historical_data"] = stock_historical_values(array[counter], period, show_plot)
            stock_data["stock_real_time_data"] = str(stock_real_time_values(array[counter]))
        else:
            counter += array_lenght
            print('Error, stock values operation not allowed')

        stock_general_data.append(stock_data)
        counter +=1

    return stock_general_data

def adjust_timestamp(original_timestamp_str, to_timezone_str):
    # Create a timezone object for the destination timezone
    to_timezone = pytz.timezone(to_timezone_str)

    # Convert the original timestamp to the desired timezone
    adjusted_timestamp = datetime.datetime.fromtimestamp(original_timestamp_str).astimezone(to_timezone)

    return adjusted_timestamp

def get_stock_price_at_timestamp(stock_symbol, timestamp):
    # Get the index for the specified stock
    stock_index = my_stocks_list_data[stock_symbol]['index']
    # Get the corresponding timezone from index_timezone
    timezone = index_timezone.get(stock_index)
    adjusted_date_time = adjust_timestamp(timestamp, timezone)
    # Format the date for Yahoo Finance query (get one day of data)
    start_date = adjusted_date_time.strftime('%Y-%m-%d')
    end_date = (adjusted_date_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    # Download historical data for the stock
    stock = yfinance.Ticker(stock_symbol)
    historical_data = stock.history(start=start_date, end=end_date, interval="1m")
    # print(historical_data)
    if historical_data.empty:
        print(f"No data available for {stock_symbol} at {start_date}")
        return None

    # print("Date time")
    # print(adjusted_date_time)
    market_opening = historical_data.index[0]
    market_close = historical_data.index[-1]
    adjusted_timestamp = int(datetime.datetime.timestamp(adjusted_date_time))
    market_opening = int(datetime.datetime.timestamp(market_opening))
    market_close = int(datetime.datetime.timestamp(market_close))
    adjusted_date_time = datetime.datetime.fromisoformat(str(adjusted_date_time))
    adjusted_date_time = adjusted_date_time.replace(second=0)
    specific_close_value = 0
    if adjusted_timestamp > market_opening and adjusted_timestamp < market_close:
        specific_close_value = historical_data.loc[adjusted_date_time, 'Close']
        print("Close value within range")
        print(specific_close_value)
    elif adjusted_timestamp < market_opening: 
        specific_close_value = str(historical_data['Close'].iloc[0])
        print("Close value previous to range")
        print(specific_close_value)
    elif adjusted_timestamp > market_close: 
        # Find the first market open date after the transaction date (next valid trading day)
        next_open_date = historical_data.index[historical_data.index > adjusted_timestamp][0]

        # Retrieve the close value for the first open day after the transaction
        specific_close_value = historical_data.loc[next_open_date, 'Close']
        # specific_close_value = str(historical_data['Close'].iloc[0])
        print("Close value post to range")
        print(specific_close_value)
        print("else")
    else:
        print("else")
        # Adjusting dates to get the previous day and next day
        # next_day = pandas.to_datetime(string_time) + timedelta(days=1)


    return specific_close_value

def compound_stocks(my_stocks_list_data):
    compound_stocks = {}
    original_aggregated_value = 0
    real_aggregated_value = 0
    percentage_change_value = 0
    print("Compound Stocks")
    print(my_stocks_list_data)

    # Iterate through the dictionary
    for stock_symbol, stock_data in my_stocks_list_data.items():
        print(f"Stock Symbol: {stock_symbol}")
        
        # Access the 'transactions' list inside each stock's data
        transactions = stock_data.get('transactions', [])
        stock_amount_invested = 0
        transaction_value = 0
        stocks_number = 0
        
        # Iterate through each transaction as if it were an array
        for index, transaction in enumerate(transactions):
            print(f"Transaction {index + 1}:")

            for key, value in transaction.items():
                print(f"  {key}: {value}")
                # Check if the key is 'cost'
                if key == 'cost':
                    # Add the value to the cost sum
                    stock_amount_invested += value
                    transaction_value = value
                if key == 'timestamp':
                    price_at_timestamp = float(get_stock_price_at_timestamp(stock_symbol, value))
                    # price_at_timestamp = 0
                    print("Price at timestamp")
                    print(price_at_timestamp)
                    print("Stocks transactioned")
                    stocks_transactioned = transaction_value / price_at_timestamp
                    stocks_number += stocks_transactioned
                    print(stocks_transactioned)
                    # print(f"Stock price of {stock_symbol} at timestamp {value} was: {price_at_timestamp}")

            print()  # Empty line for better readability between transactions
        print("Stock amount invested")
        print(stock_amount_invested)
        original_aggregated_value += stock_amount_invested
        print("Stock numbers after all transactions")
        print(stocks_number)
        print("stocks current value")
        stock_value_now = stock_real_time_values(stock_symbol)
        stock_value_now_money = stocks_number * stock_value_now["Current $"]
        print(stock_value_now_money)
        real_aggregated_value += stock_value_now_money 
        print("Percentage of change")
        change = stock_value_now_money / stock_amount_invested
        # percentage_change = (change/100)*100
        print(change)
    
    print("Valor original") #valor de inversion original
    print(original_aggregated_value)
    print("Cambio agregado") #valor de inversion real
    print(real_aggregated_value)
    print("Porcentaje cambio") #porcentaje de cambio
    percentage_change_value = real_aggregated_value / original_aggregated_value
    print(percentage_change_value)
    print("----------------------------------")
    return 0
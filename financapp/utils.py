import re
import pandas
from stocks_operations import stock_real_time_values, stock_historical_values
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
            stock_data["stock_real_time_data"] = stock_real_time_values(array[counter])
        elif(operation == 'historical_and_real_time'):
            stock_data["stock_ticker"] = array[counter]
            stock_data["stock_historical_data"] = stock_historical_values(array[counter], period, show_plot)
            stock_data["stock_real_time_data"] = stock_real_time_values(array[counter])
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
    if historical_data.empty:
        print(f"No data available for {stock_symbol} at {start_date}")
        return None

    market_opening = historical_data.index[0]
    market_close = historical_data.index[-1]
    adjusted_timestamp = int(datetime.datetime.timestamp(adjusted_date_time))
    market_opening = int(datetime.datetime.timestamp(market_opening))
    market_close = int(datetime.datetime.timestamp(market_close))
    adjusted_date_time = datetime.datetime.fromisoformat(str(adjusted_date_time))
    adjusted_date_time = adjusted_date_time.replace(second=0)
    specific_close_value = 0
    if adjusted_timestamp >= market_opening and adjusted_timestamp <= market_close:
        specific_close_value = historical_data.loc[adjusted_date_time, 'Close']
    elif adjusted_timestamp < market_opening: 
        specific_close_value = str(historical_data['Close'].iloc[0])
    elif adjusted_timestamp > market_close: 
        # Initial day counter, starting from the next day
        day_counter = 1
        valid_data_found = False
        specific_close_value = None

        while not valid_data_found:
            # Calculate the next day for searching
            next_search_date = adjusted_date_time + datetime.timedelta(days=day_counter)
            
            # Check if we're trying to search in the future beyond today
            if next_search_date.date() > datetime.datetime.now().date():
                print(f"No future trading data available beyond {datetime.datetime.now().date()}")
                return None  # Stop searching as we're in the future

            # Format the next search date range
            start_date = next_search_date.strftime('%Y-%m-%d')
            end_date = (next_search_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

            # Download historical data for the stock on the next day
            stock = yfinance.Ticker(stock_symbol)
            historical_data = stock.history(start=start_date, end=end_date, interval="1m")

            if historical_data.empty:
                print(f"No trading data found for {stock_symbol} on {start_date}. Trying the next day...")
                # Move to the next day
                day_counter += 1
            else:
                valid_data_found = True

                # Get the close value of the first valid trading minute on the next day
                next_open_date = historical_data.index[0]
                specific_close_value = historical_data.loc[next_open_date, 'Close']
    else:
        print("Not valid data found")

    return specific_close_value

def sum_transactions():
    total_sum = 0  # Initialize a variable to store the sum
    for stock, data in my_stocks_list_data.items():  # Iterate over each stock in the dictionary
        transactions = data.get('transactions', [])  # Get the transactions list
        for transaction in transactions:  # Iterate over each transaction
            total_sum += transaction.get('transaction_price', 0)  # Add the transaction price to the total sum
    return total_sum

def get_my_stock_data(stock_symbol, stock_data, original_aggregated_value, real_aggregated_value):
    # Access the 'transactions' list inside each stock's data
    transactions = stock_data.get('transactions', [])
    stock_amount_invested = 0
    transaction_value = 0
    stocks_number = 0
    
    # Iterate through each transaction as if it were an array
    for index, transaction in enumerate(transactions):

        for key, value in transaction.items():
            # Check if the key is 'cost'
            if key == 'cost':
                # Add the value to the cost sum
                stock_amount_invested += value
                transaction_value = value
            if key == 'timestamp':
                price_at_timestamp = float(get_stock_price_at_timestamp(stock_symbol, value))
                stocks_transactioned = transaction_value / price_at_timestamp
                stocks_number += stocks_transactioned

    original_aggregated_value += stock_amount_invested
    stock_value_now = stock_real_time_values(stock_symbol)
    stock_value_now_money = stocks_number * stock_value_now["Current $"]
    real_aggregated_value += stock_value_now_money 
    change = stock_value_now_money / stock_amount_invested
    percentage_change = change-1
    stock_data = {
        "stock_symbol":stock_symbol,
        "stock_currency":stock_data.get('currency'),
        "stock_invested_value": stock_amount_invested,
        "stocks_owned":stocks_number,
        "stocks_real_value":stock_value_now_money,
        "stock_change_value":change,
        "stock_change_percentage":percentage_change
    }
    stock_info = {
        "stock_data":stock_data,
        "aggregated_value":original_aggregated_value,
        "current_value":real_aggregated_value,
    }
    return stock_info

def compound_stocks(my_stocks_list_data):
    compound_stocks = {}
    original_aggregated_value = 0
    real_aggregated_value = 0

    # Iterate through the dictionary
    for stock_symbol, stock_data in my_stocks_list_data.items():
        stock_info = get_my_stock_data(stock_symbol, stock_data, original_aggregated_value, real_aggregated_value)
        original_aggregated_value = stock_info["aggregated_value"]
        real_aggregated_value = stock_info["current_value"]

        if stock_symbol not in compound_stocks:
            compound_stocks[stock_symbol] = [] 
        compound_stocks[stock_symbol].append(stock_info["stock_data"])
    
    percentage_change_value_without_transactions = real_aggregated_value / original_aggregated_value
    transactions_cost = sum_transactions()
    real_aggregated_value_transactions = real_aggregated_value - transactions_cost
    percentage_change_value_with_transactions = real_aggregated_value / original_aggregated_value
    wallet_data = {
        "wallet_invested_value":original_aggregated_value,
        "transactions_value":transactions_cost,
        "wallet_real_value_now_without_transactions":real_aggregated_value,
        "wallet_real_value_now_with_transactions":real_aggregated_value_transactions,
        "wallet_per_change_no_transactions":percentage_change_value_without_transactions,
        "wallet_per_change_with_transactions":percentage_change_value_with_transactions
    }
    wallet_stocks = {
        "wallet_value": wallet_data,
        "stocks_list": compound_stocks,
        "stocks_watchlist": {},
    }

    return wallet_stocks


def compound_stocks_daily(my_stocks_list_data):
    compound_stocks_daily = []
    daily_wallet_value = {}

    # Identify the earliest transaction date
    min_date = min(
        transaction['timestamp'] for stock_data in my_stocks_list_data.values()
        for transaction in stock_data['transactions']
    )
    start_date = datetime.datetime.fromtimestamp(min_date).date()
    end_date = datetime.datetime.now().date()

    # Loop through each day from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        daily_wallet_total = 0
        daily_transactions = []
        for stock_symbol, stock_data in my_stocks_list_data.items():
            # Get all transactions up to the current date
            total_invested = 0
            total_shares = 0

            for transaction in stock_data['transactions']:
                transaction_date = datetime.datetime.fromtimestamp(transaction['timestamp']).date()
                # If transaction date matches the current date, record the transaction
                if transaction_date == current_date:
                    daily_transactions.append({
                        "stock_symbol": stock_symbol,
                        "date": transaction_date.strftime("%Y-%m-%d"),
                        "operation": transaction['operation'],
                        "quantity": transaction['cost']
                    })
                if transaction_date <= current_date:
                    price_at_transaction = transaction.get('transaction_price', 0)
                    shares_bought = transaction['cost'] / price_at_transaction if price_at_transaction else 0
                    total_shares += shares_bought
                    total_invested += transaction['cost']

            # Fetch the stock's historical data for the current day
            stock = yfinance.Ticker(stock_symbol)
            historical_data = stock.history(start=str(current_date), end=str(current_date + timedelta(days=1)))

            if not historical_data.empty:
                daily_close_price = historical_data['Close'].iloc[-1]
                daily_stock_value = total_shares * daily_close_price
                daily_wallet_total += daily_stock_value

        if daily_wallet_total > 0:
            # Store the wallet value for the current day
            daily_wallet_total = float(daily_wallet_total)
            date_str = current_date.strftime("%Y-%m-%d")
            daily_wallet_value[date_str] = daily_wallet_total

            compound_stocks_daily.append({
                "date": date_str,
                "wallet_value": daily_wallet_total,
                # "transactions": daily_transactions
            })

        # Move to the next day
        current_date += datetime.timedelta(days=1)

    return compound_stocks_daily
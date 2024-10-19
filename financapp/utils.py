import re
import pandas
from stocks_operations import stock_real_time_values, stock_historical_values
import asyncio  # Import asyncio for async execution

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

def compound_stocks(my_stocks_list, my_stocks_list_money_invested, my_stocks_list_purchase_timestamp):
    compound_stocks = {}
    print("Stock values from stock investment")
    print(my_stocks_list)
    print(len(my_stocks_list))
    period = '1mo'
    stock_values = stocks_values(my_stocks_list,'historical_and_real_time')
    print(stock_values)
    print("----------------------------------")
    return 0
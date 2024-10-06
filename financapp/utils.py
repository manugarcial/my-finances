import re
import pandas
from stocks_operations import stock_real_time_values, stock_historical_values

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
def stocks_values(array, operation, period = '3mo', show_plot = False):
    array_lenght = len(array)
    counter = 0
    stock_returning = 0
    while array_lenght > counter:
        if(operation == 'historical'):
            stock_returning = stock_historical_values(array[counter], period, show_plot)
        elif(operation == 'real_time'):
            stock_real_time_values(array[counter])
        else:
            counter += array_lenght
            print('Error, stock values operation not allowed')
        counter +=1
    return stock_returning
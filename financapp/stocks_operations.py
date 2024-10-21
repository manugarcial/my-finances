import finnhub
import yfinance
# from utils import dataframe_into_dict
import pandas
import matplotlib.pyplot as plt
import numpy
from datetime import datetime
from scipy.signal import find_peaks
from api_keys_data import finnhub_api_key

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[36m"
ORANGE = "\033[38;5;214m"
RESET = "\033[0m"

my_finnhub_api_key = finnhub_api_key
finnhub_client = finnhub.Client(api_key=my_finnhub_api_key)

# returns if the market is opened today (Tbc: if that means that the market is opened on the same day or if it is opened atm)
def open_market(market='US'):
    response = finnhub_client.market_status(exchange=market)
    return response['isOpen']

# Obtiene calificaciones economicas de los paises del mundo (util para bonos y evoluciones de compañias que operen en la bolsa de ese pais)
def country_economy_risk(country_name):
    response = finnhub_client.country()
    # Convert list to dictionary where 'country' is the key
    country_dict = {item['country']: item for item in response}
    rating = country_dict[country_name]['rating']
    if rating == 'Aaa':
        return 1.2
    elif rating.startswith('A'):
        return 1.1
    elif rating.startswith('B'):
        return 1
    elif rating == 'C':
        return 0.8
    elif rating.startswith('C'):
        return 0.9
    else:
        print('Invalid rating')
        return 0

# stock values in real time (if market is opened, otherwise, last market values for a stock)
def stock_real_time_values(stock):
    stock_data = finnhub_client.quote(stock)
    new_keys = ['Current $', 'Change', 'Percentage change', 'Highest today', 'Lowest today', 'Open $ today', 'Prev close $', 'Timestamp']
    parsed_stock_data = dict(zip(new_keys, stock_data.values()))

    # if(parsed_stock_data['Percentage change'] > 5):
    #     print(BLUE + 'Stock: ' + stock + ' ' + str(parsed_stock_data) + RESET)
    # elif(parsed_stock_data['Percentage change'] > 0):
    #     print(GREEN + 'Stock: ' + stock + ' ' + str(parsed_stock_data) + RESET)
    # elif(parsed_stock_data['Percentage change'] < 0 and parsed_stock_data['Percentage change'] > -5):
    #     print(ORANGE + 'Stock: ' + stock + ' ' + str(parsed_stock_data) + RESET)
    # elif(parsed_stock_data['Percentage change'] < -5):
    #     print(RED + 'Stock: ' + stock + ' ' + str(parsed_stock_data) + RESET)
    # else:
    #     print('Stock: ' + stock + ' ' + str(parsed_stock_data))

    return parsed_stock_data

# Stock Historical values
def stock_historical_values(stock, period_data, show=False):
    my_stock = yfinance.Ticker(stock)
    historical_stock_data = my_stock.history(period=period_data)
    close_historical_data = historical_stock_data['Close'].values
    date_historical_data = historical_stock_data.index

    if(show): stock_historical_data_graph(stock, close_historical_data, date_historical_data)

    stock_history = {
        "stock_historic_close_data": close_historical_data
    }           

    return stock_history


# Show historical data in graph using plot library
def stock_historical_data_graph(stock, close_historical_data, date_historical_data):
    counter = 0
    new_date_historical_data = []
    date_historical_data_lenght = len(date_historical_data)
    while date_historical_data_lenght > counter:
        new_date_historical_data.append(datetime.fromisoformat(str(date_historical_data[counter])).date())
        counter += 1

    # Define the array of values (Y)
    array_values = close_historical_data

    # Create an index based on the values in the array (X)
    index_values = [str(value) for value in new_date_historical_data]

    data = pandas.Series(array_values, index=index_values)

    stop_loss = close_historical_data[-1]*0.95
    buying_oportunity = close_historical_data[-1]*1.05

    # Finding relative maxima
    peaks, _ = find_peaks(close_historical_data)
    # Finding relative minima (by finding peaks in the negative of the data)
    min_peaks, _ = find_peaks(-close_historical_data)

    max_value = max(close_historical_data)
    min_value = min(close_historical_data)
    max_index = close_historical_data.tolist().index(max_value)
    min_index = close_historical_data.tolist().index(min_value)

    # Plot the series
    plt.figure(figsize=(10, 7))  
    plt.plot(data, marker='o') 
    plt.title('Historical Stocks Graph: ' + stock)
    plt.xlabel('Index')            
    plt.ylabel('Values')  
    # Mark the maximum and minimum values
    plt.scatter(max_index, max_value, color='g', label='Max Value', zorder=5)
    plt.scatter(min_index, min_value, color='r', label='Min Value', zorder=5)
    # Annotate the max and min points
    plt.annotate(f'Max: {max_value}', xy=(max_index, max_value), xytext=(max_index, max_value + 5),
                arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10)
    plt.annotate(f'Min: {min_value}', xy=(min_index, min_value), xytext=(min_index, min_value - 15),
                arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10)
    # Mark the relative maxima
    plt.scatter(peaks, data[peaks], color='g', label='Relative Max', zorder=5)

    # Mark the relative minima
    plt.scatter(min_peaks, data[min_peaks], color='r', label='Relative Min', zorder=5)
        
    plt.axhline(y=stop_loss, color='r', linestyle='-', label='Stop Loss')
    plt.axhline(y=buying_oportunity, color='g', linestyle='-', label='Buy Opportunity')
    plt.xticks(rotation=45)       
    plt.legend()                  

    plt.show()

    return

# Calculates the last quarters surprise percentages, growth and positiveness
def surprise_percentage(company_code, quarters_limit = 5):
    response = finnhub_client.company_earnings(company_code, limit= quarters_limit)
    data_sorted = sorted(response, key=lambda x: x['period'], reverse=True)
    
    # Calculate whether surprisePercent is growing or falling
    trend = []
    for i in range(1, len(data_sorted)):
        change = data_sorted[i-1]['surprisePercent'] - data_sorted[i]['surprisePercent']
        trend.append(change)

    # Get the most recent value's surprisePercent
    most_recent = data_sorted[0]['surprisePercent']

    # Check if it is positive or negative
    is_positive = most_recent > 0

    # Return the trend and the status of the most recent value
    return {
        'trend': trend,
        'most_recent_is_positive': is_positive,
        'most_recent_surprisePercent': most_recent
    }

# Funtion to calculate RSI (Relative Strengh Index)
def calculate_rsi(data, period=14):
    """
    Function to calculate the Relative Strength Index (RSI) for a given time series.
    
    :param data: A pandas DataFrame or Series with price data (usually closing prices).
    :param period: The number of periods to use for RSI calculation (default is 14).
    :return: A pandas Series with the RSI values.
    """
    # Calculate the price differences
    delta = data.diff()
    
    # Separate the positive gains (ups) and negative losses (downs)
    gain = (delta.where(delta > 0, 0))  # Only positive changes
    loss = (-delta.where(delta < 0, 0))  # Only negative changes (inverted to be positive)
    
    # Calculate the rolling mean (exponential moving average) for gain and loss
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Calculate the Relative Strength (RS)
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

def evaluate_rsi(rsi_number):
    if(rsi_number > 70): return 0.8
    elif(rsi_number > 60): return 0.9
    elif(rsi_number > 50): return 1
    elif(rsi_number > 40): return 1.1
    else: return 1.2

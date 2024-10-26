import finnhub
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import search_dict_regex, dataframe_into_dict, html_data_into_dataframe, stocks_values, compound_stocks
from stocks_operations import calculate_rsi, open_market, country_economy_risk, surprise_percentage, evaluate_rsi
from api_keys_data import finnhub_api_key
from variables import my_18_stock_market_list, my_stocks_list, my_stocks_watchlist, my_stocks_list_purchase_timestamp, my_stocks_list_money_invested, my_stocks_list_data
import sys
import json

my_finnhub_api_key = finnhub_api_key
finnhub_client = finnhub.Client(api_key=my_finnhub_api_key)

# my_stock_market_list = my_18_stock_market_list
# my_index_dataframe = html_data_into_dataframe("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
# my_index_dict = dataframe_into_dict(my_index_dataframe)

# print("Is the stock market open today?:", open_market())
# stocks_values(my_stocks_list,'real_time','1mo')
# stocks_values(my_stocks_list,'historical', study_period, False)
# No es procesable con un script, se necesita analizar con una IA superior
# print('Company news: ' + finnhub_client.company_news('AAPL', _from="2024-01-01", to="2024-09-10"))

# matched_keys = search_dict_regex(my_index_dict, 'Adobe')
# print(matched_keys)

# --------------------------------------------------------------------------------------------------

# Example function to call compound_stocks
def main(ticker="ORCL", period='1mo'):
    stock_ticker=[]
    stock_ticker.append(ticker)
    # period len ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    study_period = period

    stock_values = stocks_values(stock_ticker,'historical_and_real_time', study_period, False)
    days_to_check_investing_options = 15
    last_stock_days_values = stock_values[-days_to_check_investing_options:]
    rsi = 0
    for stock in last_stock_days_values:
        ticker = stock['stock_ticker']
        closing_prices = stock['stock_historical_data']['stock_historic_close_data']
        rsi = int(calculate_rsi(closing_prices))
        rsi_evaluation = evaluate_rsi(rsi)

    company_profile = finnhub_client.company_profile2(symbol=stock_ticker)
    company_peers = finnhub_client.company_peers(stock_ticker)
    company_recommendations = finnhub_client.recommendation_trends(stock_ticker)
    rating_adjustment = country_economy_risk('United States') # check currency strenght
    surprise_data = surprise_percentage(stock_ticker[0])
    # Que la sorpresa baje o suba, se ha de estudiar como ponderarlo y si es bueno o malo
    company_sentiment = finnhub_client.stock_insider_sentiment(stock_ticker, '2024-01-01', '2024-09-01')
    
    stock_data = {
        "company_stock_data_values":stock_values,
        "company_relative_strengh_index_rsi":rsi,
        "company_rsi_evaluation":rsi_evaluation,
        "company_profile":company_profile,
        "company_market_competitors":company_peers,
        "company_recommendations":company_recommendations,
        "country_economy_rating":rating_adjustment,
        "company_surprise_index":surprise_data,
        "company_sentiment":company_sentiment,
    }
    return stock_data

# Run the main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
      print("Usage: single_stock.py")
      sys.exit(1)

    ticker = sys.argv[1]
    period = sys.argv[2]

    stock_data = main(ticker, period)
    print(stock_data)

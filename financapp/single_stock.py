import finnhub
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import search_dict_regex, dataframe_into_dict, html_data_into_dataframe, stocks_values, compound_stocks
from stocks_operations import calculate_rsi, open_market, country_economy_risk, surprise_percentage, evaluate_rsi
from api_keys_data import finnhub_api_key
from variables import my_18_stock_market_list, my_stocks_list, my_stocks_watchlist, my_stocks_list_purchase_timestamp, my_stocks_list_money_invested, my_stocks_list_data

my_finnhub_api_key = finnhub_api_key
finnhub_client = finnhub.Client(api_key=my_finnhub_api_key)

# my_stock_market_list = my_18_stock_market_list

stock_ticker="ORCL"

# period len ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
study_period = '1d'
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

stock_values = stocks_values(my_stocks_list,'historical_and_real_time', study_period, False)
print("stock_values")
print(stock_values)
days_to_check_investing_options = 15
last_stock_days_values = stock_values[-days_to_check_investing_options:]
print(last_stock_days_values)
stock_dataframe = pd.DataFrame(last_stock_days_values, columns=["Values"])
print(stock_dataframe)

stock_dataframe['RSI'] = calculate_rsi(stock_dataframe)
RSI_list = stock_dataframe.values.tolist()
print(RSI_list)
rsi_evaluation = evaluate_rsi(RSI_list[-1][1])
print('RSI evaluation: ', rsi_evaluation)

# company_profile = finnhub_client.company_profile2(symbol=stock_ticker)
# print("company_profile")
# print(company_profile)
# company_peers = finnhub_client.company_peers(stock_ticker)
# print("company_peers")
# print(company_peers)
# company_recommendations = finnhub_client.recommendation_trends(stock_ticker)
# print("company_recommendations")
# print(company_recommendations)
# rating_adjustment = country_economy_risk('United States') # check currency strenght
# print("rating_adjustment")
# print(rating_adjustment)
# surprise_data = surprise_percentage('NVDA')
# print("surprise_data") 
# print(surprise_data) # Que la sorpresa baje o suba, se ha de estudiar como ponderarlo y si es bueno o malo
# company_sentiment = finnhub_client.stock_insider_sentiment(stock_ticker, '2024-01-01', '2024-09-01')
# print('Stock insider sentiment')
# print(company_sentiment) # TBD como interpretar los valores change y mspr a lo largo del tiempo
import finnhub
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import search_dict_regex, dataframe_into_dict, html_data_into_dataframe, stocks_values
from stocks_operations import calculate_rsi, open_market, country_economy_risk, surprise_percentage, evaluate_rsi
from api_keys_data import finnhub_api_key
from variables import my_18_stock_market_list, my_stocks_list, my_stocks_watchlist

my_finnhub_api_key = finnhub_api_key
finnhub_client = finnhub.Client(api_key=my_finnhub_api_key)

my_stock_market_list = my_18_stock_market_list

# period len ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
study_period = '6mo'
my_index_dataframe = html_data_into_dataframe("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
my_index_dict = dataframe_into_dict(my_index_dataframe)

# print("Is the stock market open today?:", open_market())
stocks_values(my_stocks_list,'real_time')
stocks_values(my_stocks_list,'historical', study_period, False)
rating_adjustment = country_economy_risk('United States')
surprise_data = surprise_percentage('NVDA')
# Que la sorpresa baje o suba, se ha de estudiar como ponderarlo y si es bueno o malo
print('Surprise data: ', surprise_data)
# TBD como interpretar los valores change y mspr a lo largo del tiempo
print('Stock insider sentiment: ', finnhub_client.stock_insider_sentiment('AAPL', '2024-01-01', '2024-09-01'))
# No es procesable con un script, se necesita analizar con una IA superior
# print('Company news: ' + finnhub_client.company_news('AAPL', _from="2024-01-01", to="2024-09-10"))
# Nos proporciona info general sobre la empresa
print('Company profile: ', finnhub_client.company_profile2(symbol='AAPL'))
# Nos proporciona Ticker sobre la competencia (puede ser util para valorar el estado del mercado en cuanto al nicho de operaciones)
print('Company peers: ', finnhub_client.company_peers('AAPL'))
# Nos proporciona informacion sobre recomendaciones (tomarlo con cuidado, hay que verificar quienes dan estas recomendaciones)
print('Company recommendation trends: ', finnhub_client.recommendation_trends('AAPL'))

# matched_keys = search_dict_regex(my_index_dict, 'Adobe')
# print(matched_keys)

stock_values = stocks_values(my_stocks_list,'historical', study_period, False)

days_to_check_investing_options = 15
last_stock_days_values = stock_values[-days_to_check_investing_options:]
stock_dataframe = pd.DataFrame(last_stock_days_values, columns=["Values"])

stock_dataframe['RSI'] = calculate_rsi(stock_dataframe)
RSI_list = stock_dataframe.values.tolist()
rsi_evaluation = evaluate_rsi(RSI_list[-1][1])
print('RSI evaluation: ', rsi_evaluation)

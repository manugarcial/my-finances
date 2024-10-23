# Sample data

my_18_stock_market_list = {
    'S&P500':'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
    'Nasdaq_100':'https://en.wikipedia.org/wiki/NASDAQ-100', 
    'Dow_Jones':'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average', 
    'FTSE_100':'https://en.wikipedia.org/wiki/FTSE_100_Index', 
    'DAX_40':'https://en.wikipedia.org/wiki/DAX', 
    'CAC_40':'https://en.wikipedia.org/wiki/CAC_40', 
    'Nikkei_225':'https://en.wikipedia.org/wiki/Nikkei_225', 
    'Shanghai_SE':' https://en.wikipedia.org/wiki/Shanghai_Stock_Exchange', 
    'Hang_SI':'https://en.wikipedia.org/wiki/Hang_Seng_Index', 
    'BSE_Sensex':'https://en.wikipedia.org/wiki/BSE_SENSEX', 
    'TSX_Composite':'https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index', 
    'ASX_200':'https://en.wikipedia.org/wiki/S%26P/ASX_200', 
    'TSX_60':'https://en.wikipedia.org/wiki/S%26P/TSX_60', 
    'SSE_Composite':'https://en.wikipedia.org/wiki/SSE_Composite_Index', 
    'KOSPI':'https://en.wikipedia.org/wiki/KOSPI', 
    'IBEX_35':'https://en.wikipedia.org/wiki/IBEX_35', 
    'SWISS_MI':'https://en.wikipedia.org/wiki/Swiss_Market_Index', 
    'MIB':'https://en.wikipedia.org/wiki/FTSE_MIB'
}

# my_stocks_list = ['AAPL','ORCL','COST','TSLA','ORLY','MSI','HWKN','MCO','META','AMZN','NVDA']
my_stocks_list = ['AAPL','ORCL','COST']
my_stocks_list_money_invested = [10, 30, 35]
my_stocks_list_purchase_timestamp = ['1729090040','1729003640','1728917240']
# Operations considered: invest, withdraw
# my_stocks_list_data = {
#     'AAPL': {'index':'Nasdaq100','transactions':[{'operation':'invest', 'cost':50, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729250200}, 
#                              {'operation':'withdraw', 'cost':-30, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 232, 'timestamp':1729263200}, 
#                              {'operation':'invest', 'cost':80, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 234, 'timestamp':1729280200}]},
#     'ORCL': {'index':'Nasdaq100','transactions':[{'operation':'invest', 'transaction_price':1.10, 'cost':100, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729250200}, 
#                              {'operation':'withdraw', 'cost':-20, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 232, 'timestamp':1729263200}, 
#                              {'operation':'invest', 'cost':50, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 234, 'timestamp':1729280200}]},
#     'COST': {'index':'Nasdaq100','transactions':[{'operation':'invest', 'cost':10, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729250200},  
#                              {'operation':'invest', 'cost':50, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 234, 'timestamp':1729280200}]}
# }
# my_stocks_list_data = {
#     'AAPL': {'index':'Nasdaq100','transactions':[{'operation':'invest', 'cost':50, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729263200},
#                                                  {'operation':'withdraw', 'cost':-30, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 232, 'timestamp':1729263200},
#                                                  {'operation':'invest', 'cost':100, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729250200},
#                                                  {'operation':'invest', 'cost':100, 'transaction_price':1.10, 'currency':'US Dollars', 'stock_price': 230,'timestamp':1729290200}]}
# }
my_stocks_list_data = {
    'AAPL': {'index':'Nasdaq100','currency':'US Dollars','transactions':[{'operation':'invest', 'cost':10, 'transaction_price':0, 'stock_price': 0,'timestamp':1727875800}]},
    'ORCL': {'index':'Nasdaq100','currency':'US Dollars','transactions':[{'operation':'invest', 'cost':10, 'transaction_price':1.10, 'stock_price': 0,'timestamp':1727883300}]},
    'COST': {'index':'Nasdaq100','currency':'US Dollars','transactions':[{'operation':'invest', 'cost':10, 'transaction_price':1.10, 'stock_price': 0,'timestamp':1728567000}]}
}
index_timezone = {'Nasdaq100':'America/New_York','SP500':'America/New_York'}
my_stocks_watchlist = ['ADBE','ABNB','ASML','COST','INTC','MSFT','PANW','PEP','KO','AMD']
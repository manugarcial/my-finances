from utils import compound_stocks, compound_stocks_daily
from variables import my_stocks_list_data
from stocks.stock_db_operations import select_user_transactions
import sys

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def transform_stock_tuple(stock_tuple):
    # Mapping for index and currency values
    index_mapping = {
        'NASDAQ': 'Nasdaq100',
        'NYSE': 'New York Stock Exchange'
    }

    currency_mapping = {
        'USD': 'US Dollars',
        'EUR': 'Euros'
    }

    # Unpack the tuple into separate variables
    stock_symbol, index, currency, operation, cost, transaction_price, stock_price, timestamp = stock_tuple

    # Construct the dictionary
    transformed_data = {
        stock_symbol: {
            'index': index_mapping.get(index, 'Unknown Index'),
            'currency': currency_mapping.get(currency, 'Unknown Currency'),
            'transactions': [
                {
                    'operation': operation,
                    'cost': cost,
                    'transaction_price': transaction_price,
                    'stock_price': stock_price,
                    'timestamp': timestamp
                }
            ]
        }
    }

    return transformed_data

# Example function to call compound_stocks
def main():
    database_transactions = select_user_transactions(username)
    my_stocks_list = {}
    for transaction in database_transactions:
        stock_symbol = transaction[0]
        index = transaction[1]
        currency = transaction[2]
        operation = transaction[3]
        cost = transaction[4]
        transaction_price = transaction[5]
        stock_price = transaction[6]
        timestamp = transaction[7]

        # Check if the stock_symbol already exists in the dictionary
        if stock_symbol not in my_stocks_list:
            # Initialize it if it doesn't exist
            my_stocks_list[stock_symbol] = {
                'index': index,
                'currency': currency,
                'transactions': []  # Initialize an empty list for transactions
            }
        
        # Create the new transaction entry
        new_transaction = {
            'operation': operation,
            'cost': cost,
            'transaction_price': transaction_price,
            'stock_price': stock_price,
            'timestamp': timestamp
        }

        # Append the new transaction to the list of transactions for the stock
        my_stocks_list[stock_symbol]['transactions'].append(new_transaction)

    # print("my stock")
    # print(my_stocks_list)

    compound = compound_stocks(my_stocks_list)
    compound_daily = compound_stocks_daily(my_stocks_list)

    # print(compound)
    # print(compound_daily)
    # print("-------")

    # try:
    #     compound_daily = compound_stocks_daily(my_stocks_list)
    #     print("Compound Daily:")
    #     print(compound_daily)
    # except Exception as e:
    #     print("An error occurred:", e)

    wallet_data = {
        "compound_stocks_real_time":compound,
        "compound_stocks_daily":compound_daily,
    }
    # print("het")
    # print(compound_stocks_daily(my_stocks_list))
    print(wallet_data)

# Run the main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: stocks_investment.py")
        sys.exit(1)

    # Datos iniciales
    username = sys.argv[1]
    main()

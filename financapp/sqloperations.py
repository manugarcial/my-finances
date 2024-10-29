import sqlite3
from api_keys_data import finnhub_api_key, my_sql_db

my_finnhub_api_key = finnhub_api_key
sql_db = my_sql_db

def show_db_dables():
   # Connect to the SQLite database
    sql_connection = sqlite3.connect(sql_db)
    cursor = sql_connection.cursor()

    # Query to list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    # Close the connection
    sql_connection.close()

def select_all_stock_transactions():
  sql_connection = sqlite3.connect(sql_db)
  cursor = sql_connection.cursor()

  cursor.execute("""
      SELECT stocks.ticker, stocks.stock_index, stocks.currency, transactions.operation, transactions.cost, transactions.transaction_price, transactions.stock_price, transactions.timestamp
      FROM stocks
      JOIN transactions ON stocks.ticker = transactions.ticker
  """)

  rows = cursor.fetchall()
  for row in rows:
      print(row)

  sql_connection.close()

def insert_new_stock_transactions(ticker,stock_data):
  sql_connection = sqlite3.connect(sql_db)
  cursor = sql_connection.cursor()

  # Insert stock data into stocks table
  cursor.execute("""
      INSERT OR IGNORE INTO stocks (ticker, stock_index, currency)
      VALUES (?, ?, ?)
  """, (ticker, stock_data['index'], stock_data['currency']))

  # Insert transaction data into transactions table for the specific stock
  for transaction in stock_data['transactions']:
  # Insert transaction and handle duplicates
    try:
        cursor.execute("""
            INSERT INTO transactions (ticker, operation, cost, transaction_price, stock_price, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticker, transaction['operation'], transaction['cost'], transaction['transaction_price'],
              transaction['stock_price'], transaction['timestamp']))

        sql_connection.commit()

    except sqlite3.IntegrityError:
        print("A transaction with this ticker and timestamp already exists. Duplicate avoided.")

  # Commit the changes and close the connection
  sql_connection.commit()
  sql_connection.close()

def modify_stock_investment_transaction_data(new_invesment_value, ticker_value, timestemp_value):
  sql_connection = sqlite3.connect(sql_db)
  cursor = sql_connection.cursor()

  cursor.execute("UPDATE transactions SET cost = ? WHERE ticker = ? AND timestamp = ?", (new_invesment_value, ticker_value, timestemp_value))
  
  sql_connection.commit()
  sql_connection.close()

def delete_stock_transaction(ticker, timestamp):
  sql_connection = sqlite3.connect('my_stocks.db')
  cursor = sql_connection.cursor()

  cursor.execute("DELETE FROM transactions WHERE ticker = ? AND timestamp = ?", (ticker, timestamp))

  sql_connection.commit()
  sql_connection.close()


# Run the main function
if __name__ == "__main__":
  ticker = 'AAPL'
  stock_data = {
      'index': 'Nasdaq100',
      'currency': 'US Dollars',
      'transactions': [
          {
              'operation': 'invest',
              'cost': 10,
              'transaction_price': 0,
              'stock_price': 0,
              'timestamp': 1727975800
          }
      ]
  }
  # show_db_dables()
  print("-----------------------------------------------------")
  insert_new_stock_transactions(ticker, stock_data)
  print("-----------------------------------------------------")
  select_all_stock_transactions()
  print("-----------------------------------------------------")
  modify_stock_investment_transaction_data(25,'AAPL',1727975800)
  print("-----------------------------------------------------")
  select_all_stock_transactions()
  print("-----------------------------------------------------")

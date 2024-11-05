from flask import jsonify
import psycopg2
# from postgreconnection import my_sql_db
from sqlalchemy.orm import joinedload

sql_db = "postgresql://financappdb_owner:2iwWjrP4IEhB@ep-long-poetry-a2wbgphc.eu-central-1.aws.neon.tech/financappdb?sslmode=require"  # PostgreSQL connection string

def select_all_transactions():
    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()
        
        # Execute the SELECT query, including the username
        cursor.execute("""
            SELECT s.ticker, s.stock_index, s.currency, 
                   t.username, t.operation, t.cost, 
                   t.transaction_price, t.stock_price, 
                   t.timestamp
            FROM stocks s
            JOIN transactions t ON s.ticker = t.ticker;
        """)
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the results
        print("All Stock Transactions:")
        for row in rows:
            print(row)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
            sql_connection.close()

def select_user_transactions(username):
    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()
        
        # Execute the SELECT query for a specific user
        cursor.execute("""
            SELECT s.ticker, s.stock_index, s.currency, 
                   t.operation, t.cost, 
                   t.transaction_price, t.stock_price, 
                   t.timestamp
            FROM stocks s
            JOIN transactions t ON s.ticker = t.ticker
            WHERE t.username = %s;  -- Filter by username
        """, (username,))
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the results
        if rows:
            # print(f"All Stock Transactions for User '{username}':")
            # for row in rows:
            #     print(row)
            
            return rows
        else:
            print(f"No transactions found for user '{username}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
            sql_connection.close()

# Function to validate the stock ticker
def is_valid_stock(ticker):
    # Here, you can implement logic to validate the stock.
    # For example, check against a list of known valid tickers or make an API call.
    # This is a placeholder implementation. You need to replace it with your actual validation logic.
    valid_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']  # Example list of valid stocks
    return ticker in valid_stocks

def insert_single_transaction(user_id, ticker, stock_index, currency, operation, cost, transaction_price, stock_price, timestamp):
    # Check if the stock is valid before proceeding
    if not is_valid_stock(ticker):
        raise ValueError(f"The stock '{ticker}' is not a valid stock.")

    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()

        print("insert_single_transaction inside sql connection")

        # First, check if the stock exists; if not, insert it
        cursor.execute("""
            INSERT INTO stocks (ticker, stock_index, currency)
            VALUES (%s, %s, %s)
            ON CONFLICT (ticker) DO NOTHING;
        """, (ticker, stock_index, currency))

        # Insert the transaction associated with the stock
        try:
            print("insert_single_transaction inside transaction")
            cursor.execute("""
                INSERT INTO transactions (username, ticker, operation, cost, transaction_price, stock_price, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (user_id, ticker, operation, cost, transaction_price, stock_price, timestamp))
            sql_connection.commit()  # Commit the transaction insertion
        except psycopg2.IntegrityError as e:
            print(f"A transaction with this ticker and timestamp already exists. Duplicate avoided. Error: {e}")
            sql_connection.rollback()  # Rollback if there's a duplicate

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
            sql_connection.close()


def modify_stock_cost_transaction_data(new_investment_value, ticker_value, timestamp_value, user_id):
    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()

        # Execute the update statement
        cursor.execute("""
            UPDATE transactions 
            SET cost = %s 
            WHERE ticker = %s AND timestamp = %s AND username = %s;
        """, (new_investment_value, ticker_value, timestamp_value, user_id))

        # Commit the changes
        sql_connection.commit()
        
        # Check if the update affected any rows
        if cursor.rowcount == 0:
            print("No transaction found with the specified criteria. Update failed.")
        else:
            print("Transaction updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
            sql_connection.close()

def delete_stock_transaction(ticker, timestamp, user_id):
    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()

        # Execute the delete statement
        cursor.execute("""
            DELETE FROM transactions 
            WHERE ticker = %s AND timestamp = %s AND username = %s;
        """, (ticker, timestamp, user_id))

        # Commit the changes
        sql_connection.commit()
        
        # Check if the delete affected any rows
        if cursor.rowcount == 0:
            print("No transaction found with the specified criteria. Delete failed.")
        else:
            print("Transaction deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
            sql_connection.close()

# Run the main function
if __name__ == "__main__":
    user_id = "test101"  # Replace with actual username
    ticker = "AAPL"
    stock_index = "NASDAQ"
    currency = "USD"
    operation = "buy"
    cost = 1500.00
    transaction_price = 190.00
    stock_price = 45.00
    timestamp = 1738316800  # Example Unix timestamp

    new_investment_value = 1600.00
    ticker_value = "AAPL"
    timestamp_value = 1738316800  # Example Unix timestamp

    # modify_stock_cost_transaction_data(new_investment_value, ticker_value, timestamp_value, user_id)
    # delete_stock_transaction(ticker_value, timestamp_value, user_id)

    # try:
    #     insert_single_transaction(user_id, ticker, stock_index, currency, operation, cost, transaction_price, stock_price, timestamp)
    #     print("Transaction inserted successfully.")
    # except ValueError as ve:
    #     print(ve)  # Handle the case where the stock is invalid
    # except Exception as e:
    #     print(f"Failed to insert transaction: {e}")

    # show_db_tables()
    print("-----------------------------------------------------")
    # insert_new_stock_transactions(ticker, stock_data)
    # print("-----------------------------------------------------")
    select_all_transactions()
    # insert_new_stock_transactions()
    print("-----------------------------------------------------")
    # # modify_stock_investment_transaction_data(25,'AAPL',1727975800)
    # # print("-----------------------------------------------------")
    # select_all_users()
    # print("-----------------------------------------------------")

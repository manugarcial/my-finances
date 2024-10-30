import psycopg2
from postgreconnection import my_sql_db

sql_db = my_sql_db  # PostgreSQL connection string

def show_db_tables():
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    cursor.close()
    sql_connection.close()

def select_all_stock_transactions():
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("""
        SELECT stocks.ticker, stocks.stock_index, stocks.currency, 
               transactions.operation, transactions.cost, 
               transactions.transaction_price, transactions.stock_price, 
               transactions.timestamp, transactions.user_id
        FROM stocks
        JOIN transactions ON stocks.ticker = transactions.ticker;
    """)
    rows = cursor.fetchall()
    print("All Stock transactions:")
    for row in rows:
        print(row)
    cursor.close()
    sql_connection.close()

def select_all_users():
    # Establish a connection to the database
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()

    # Execute the query to select all users
    cursor.execute("SELECT * FROM users;")
    
    # Fetch all rows from the executed query
    users = cursor.fetchall()
    
    # Print the results
    print("All Users:")
    for user in users:
        print(user)

    # Close the cursor and connection
    cursor.close()
    sql_connection.close()

def add_user(name, surname, username, password_hash, email):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("""
        INSERT INTO users (name, surname, username, password_hash, email) 
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (username, email) DO NOTHING;
    """, (name, surname, username, password_hash, email))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def delete_user(user_id):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def modify_user(user_id, name=None, surname=None, username=None, password_hash=None, email=None):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    fields = []
    values = []
    
    if name:
        fields.append("name = %s")
        values.append(name)
    if surname:
        fields.append("surname = %s")
        values.append(surname)
    if username:
        fields.append("username = %s")
        values.append(username)
    if password_hash:
        fields.append("password_hash = %s")
        values.append(password_hash)
    if email:
        fields.append("email = %s")
        values.append(email)
        
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def insert_new_stock_transactions(user_id, ticker, stock_data):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()

    cursor.execute("""
        INSERT INTO stocks (ticker, stock_index, currency)
        VALUES (%s, %s, %s)
        ON CONFLICT (ticker) DO NOTHING;
    """, (ticker, stock_data['index'], stock_data['currency']))

    for transaction in stock_data['transactions']:
        try:
            cursor.execute("""
                INSERT INTO transactions (ticker, user_id, operation, cost, transaction_price, stock_price, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, timestamp) DO NOTHING;
            """, (ticker, user_id, transaction['operation'], transaction['cost'],
                  transaction['transaction_price'], transaction['stock_price'], transaction['timestamp']))
            sql_connection.commit()
        except psycopg2.IntegrityError as e:
            print(f"A transaction with this ticker and timestamp already exists. Duplicate avoided. Error: {e}")
            sql_connection.rollback()

    cursor.close()
    sql_connection.close()

def modify_stock_investment_transaction_data(new_investment_value, ticker_value, timestamp_value, user_id):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("""
        UPDATE transactions 
        SET cost = %s 
        WHERE ticker = %s AND timestamp = %s AND user_id = %s;
    """, (new_investment_value, ticker_value, timestamp_value, user_id))
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

def delete_stock_transaction(ticker, timestamp, user_id):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    cursor.execute("""
        DELETE FROM transactions 
        WHERE ticker = %s AND timestamp = %s AND user_id = %s;
    """, (ticker, timestamp, user_id))
    sql_connection.commit()
    cursor.close()
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

    show_db_tables()
    print("-----------------------------------------------------")
    # insert_new_stock_transactions(ticker, stock_data)
    # print("-----------------------------------------------------")
    select_all_stock_transactions()
    print("-----------------------------------------------------")
    # modify_stock_investment_transaction_data(25,'AAPL',1727975800)
    # print("-----------------------------------------------------")
    select_all_users()
    print("-----------------------------------------------------")

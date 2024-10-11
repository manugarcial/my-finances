import sqlite3

def create_table_db(table_name, *fields):
    sql_connection = sqlite3.connect('financapp.db')
    cursor = sql_connection.cursor()

    if len(fields) == 0:
        print("Error: No fields specified")
        return
    
    # Construct the fields part of the SQL statement
    fields_str = ', '.join(fields)

    # Define the SQL query to create the table dynamically
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {fields_str}
    )
    '''

    try:
        # Execute the SQL query to create the table
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created or already exists with fields: {fields_str}.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Commit the transaction and close the connection
        sql_connection.commit()
        sql_connection.close()

    return

def alter_table_db(table_name, *fields):
    sql_connection = sqlite3.connect('financapp.db')
    cursor = sql_connection.cursor()

    if len(fields) == 0:
        print("Error: At least one column must be specified.")
        return

    try:
        # Alter the table for each field
        for field in fields:
            alter_table_query = f'ALTER TABLE {table_name} ADD COLUMN {field}'
            cursor.execute(alter_table_query)
            print(f"Column '{field}' added to table '{table_name}'.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        sql_connection.commit()
        sql_connection.close()

    return

def drop_table_db(table_name):
    sql_connection = sqlite3.connect('financapp.db')
    cursor = sql_connection.cursor()

    drop_table_query = f'DROP TABLE IF EXISTS {table_name}'

    try:
        cursor.execute(drop_table_query)
        print(f"Table '{table_name}' deleted if it existed.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        sql_connection.commit()
        sql_connection.close()

    return


# Example usage: Create a table named 'employees' with fields 'first_name TEXT', 'last_name TEXT', and 'salary REAL'
create_table_db('stocks', 'first_name TEXT', 'last_name TEXT', 'salary REAL')

# Example usage for altering a table:
alter_table_db('stocks', 'address TEXT', 'phone_number TEXT')

# Example usage for dropping a table:
drop_table_db('stocks')
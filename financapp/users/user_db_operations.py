from flask import jsonify
import psycopg2
# from postgreconnection import my_sql_db
from sqlalchemy.orm import joinedload

sql_db = "postgresql://financappdb_owner:2iwWjrP4IEhB@ep-long-poetry-a2wbgphc.eu-central-1.aws.neon.tech/financappdb?sslmode=require"  # PostgreSQL connection string

def user_login(username):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    # Fetch the user and validate password
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    sql_connection.close()
    return user

def user_register(username, hashed_password, name, surname, email):
    sql_connection = psycopg2.connect(sql_db)
    cursor = sql_connection.cursor()
    try: 
        print("entro en user registration try")
        cursor.execute("""
            INSERT INTO users (name, surname, username, password_hash, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, surname, username, hashed_password, email)) 
        sql_connection.commit()
    except psycopg2.IntegrityError:
        sql_connection.rollback()

    cursor.close()
    sql_connection.close()

def check_permission(user_id, permission_name):
    try:
        # Connect to the PostgreSQL database
        sql_connection = psycopg2.connect(sql_db)
        cursor = sql_connection.cursor()
        
        # SQL query to get the user's roles and associated permissions
        query = """
        SELECT p.permission_name
        FROM users u
        JOIN user_roles ur ON u.id = ur.user_id
        JOIN roles r ON ur.role_id = r.id
        JOIN role_permissions rp ON r.id = rp.role_id
        JOIN permissions p ON rp.permission_id = p.id
        WHERE u.id = %s;
        """
        
        cursor.execute(query, (user_id,))
        permissions = cursor.fetchall()

        # Check if the specified permission exists
        for permission in permissions:
            if permission[0] == permission_name:
                return True
        
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if sql_connection:
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

# Run the main function
if __name__ == "__main__":
    # print("-----------------------------------------------------")
    select_all_users()
    # print("-----------------------------------------------------")

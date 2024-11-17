from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess  # To execute Python scripts
from flasgger import Swagger
from api_keys_data import jwt_secret_key
from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from users.user_db_operations import user_login, user_register
from stocks.stock_db_operations import insert_single_transaction
import psycopg2
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Needed for executing raw SQL queries

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)
# Set the database URI directly using the connection string from Neon.tech
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://financappdb_owner:2iwWjrP4IEhB@ep-long-poetry-a2wbgphc.eu-central-1.aws.neon.tech/financappdb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids overhead

# CORS(app)  # Enable CORS for all routes
allowed_origins = ['http://localhost:8080', 'https://my-finances-nu.vercel.app']
# Configure CORS to allow only the specified origins
CORS(app, resources={r"/*": {"origins": allowed_origins}})
swagger = Swagger(app) 
jwt = JWTManager(app)

# Initialize the database
db = SQLAlchemy(app)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour"]
)
    
@app.route('/list_tables')
@limiter.limit("1 per day")
def list_tables():
    try:
        # Reflect the database schema to get all tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        return f"Tables in the database: {tables}"
    except Exception as e:
        return f"Error: {e}"

# Register a new user (for demo purposes, use a database in production)
@app.route('/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')  # This should be hashed in production
    name = data.get('name', '')
    surname = data.get('surname', '')
    email = data.get('email', '')
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)
    try:
        print(hashed_password)
        user_register(username, hashed_password, name, surname, email)
        return jsonify({"msg": "User registered successfully"}), 201
    
    except psycopg2.Error as e:
        return jsonify({"msg": "Database error", "error": str(e)}), 500

# User login
@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    try: 
        user = user_login(username)
        if user and check_password_hash(user[0], password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Invalid username or password"}), 401

    except psycopg2.Error as e:
        return jsonify({"msg": "Database error", "error": str(e)}), 500

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/stocks_investment', methods=['POST'])
@limiter.limit("5 per minute")
def stocks():
    """
    Home endpoint to return available scripts.
    ---
    responses:
      200:
        description: A list of available scripts
    """
    data = request.get_json()
    try:
        username = data.get('username')
        # You can use subprocess to run the script
        result = subprocess.run(['python3', 'stocks_investment.py', username], capture_output=True, text=True)
        # print("result from app.py")
        # print(result.stdout)
        return jsonify({"wallet": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/add_stock', methods=['POST'])
@limiter.limit("6 per minute")
def add_stock():
    data = request.json
    try:
        # Call the function to insert a new transaction
        insert_single_transaction(
            user_id=data['user_id'],
            ticker=data['stock_symbol'],
            stock_index=data['stock_index'],
            currency=data['currency'],
            operation=data['operation'],
            cost=data['cost'],
            transaction_price=data['transaction_price'],
            stock_price=data['stock_price'],
            timestamp=data['timestamp']
        )
        return jsonify({"message": "Transaction inserted successfully"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to insert transaction"}), 500
    
@app.route('/single_stock', methods=['POST'])
@limiter.limit("5 per minute")
def single_stock():
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        period = data.get('period')
        # You can use subprocess to run the script
        result = subprocess.run(['python3', 'single_stock.py', ticker, period], capture_output=True, text=True)

        return jsonify({"stock": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/calculate_irpf', methods=['POST'])
@limiter.limit("30 per minute")
def irpf():
    """
    Calculate IRPF based on the provided data.
    ---
    parameters:
      - name: category
        in: body
        required: true
        type: string
        description: The category for calculation (e.g., technology, finance, health)
      - name: quantity
        in: body
        required: true
        type: integer
        description: The quantity for the calculation
    responses:
      200:
        description: A response containing the processed data
        schema:
          type: object
          properties:
            output:
              type: string
              description: The processed output data
      400:
        description: Bad request
    """
    try:
        data = request.get_json()
        
        salary = data.get('salary')
        currency = data.get('currency')
        country_code = data.get('country')
        region_code = data.get('region')
        anual_rent = data.get('anual_rent')
        health_discount = data.get('health')
        
        # Here you could use the data to pass to your script if needed
        # For now, just simulate a response
        
        # Example: Call your calculate_irpf.py with the parameters
        result = subprocess.run(
            ['python3', 'calculate_irpf.py', str(salary), currency, country_code, region_code, str(anual_rent), str(health_discount)],
            capture_output=True, text=True
        )

        output = result.stdout

        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/calculate_mortgage', methods=['POST'])
@limiter.limit("30 per minute")
def mortgage():
    try:
        data = request.get_json()
        
        capital = data.get('capital')
        interest = data.get('interest')
        mortgage_years = data.get('mortgage_years')
        additional_yearly_payment = data.get('additional_yearly_payment')
        start_payment_year = data.get('start_payment_year')
        purchase_tax = data.get('purchase_tax')
        sell_price = data.get('sell_price')
        bank_finance_percentage = data.get('bank_finance_percentage')
        agency_commission = data.get('agency_commission')
        
        # Here you could use the data to pass to your script if needed
        # For now, just simulate a response

        result = subprocess.run(
            ['python3', 'mortgage.py', str(capital), str(interest), str(mortgage_years), str(additional_yearly_payment), str(start_payment_year), str(purchase_tax), str(sell_price), str(bank_finance_percentage), str(agency_commission)],
            capture_output=True, text=True
        )

        # Check for errors in the script execution
        if result.returncode != 0:
            return jsonify({"error": "Script execution failed", "details": result.stderr}), 500

        output = result.stdout

        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

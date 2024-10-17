from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess  # To execute Python scripts
from flasgger import Swagger

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
swagger = Swagger(app) 

@app.route('/')
def home():
    return jsonify({
        "scripts": [
            {"name": "investments", "url": "/investing.py"},
            {"name": "irpf", "url": "/calculate_irpf.py"},
            {"name": "mortgage", "url": "/mortgage.py"},
        ]
    })

@app.route('/investing.py')
def investments():
    """
    Home endpoint to return available scripts.
    ---
    responses:
      200:
        description: A list of available scripts
    """
    try:
        # You can use subprocess to run the script
        result = subprocess.run(['python3', 'investing.py'], capture_output=True, text=True)
        print("Script output:", result.stdout)
        return jsonify({"output": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/calculate_irpf', methods=['POST'])
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
        age = data.get('age')
        anual_rent = data.get('anual_rent')
        health_discount = data.get('health')
        
        # Here you could use the data to pass to your script if needed
        # For now, just simulate a response
        
        # Example: Call your calculate_irpf.py with the parameters
        result = subprocess.run(
            ['python3', 'calculate_irpf.py', str(salary), currency, country_code, region_code, str(age), str(anual_rent), str(health_discount)],
            capture_output=True, text=True
        )

        # Check for errors in the script execution
        if result.returncode != 0:
            return jsonify({"error": "Script execution failed", "details": result.stderr}), 500

        output = result.stdout

        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/calculate_mortgage', methods=['POST'])
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
        print(result.stdout)

        # Check for errors in the script execution
        if result.returncode != 0:
            return jsonify({"error": "Script execution failed", "details": result.stderr}), 500

        output = result.stdout

        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

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
            {"name": "Script 1", "url": "/investing.py"},
            {"name": "Script 2", "url": "/calculate_irpf.py"},
            # {"name": "Script 3", "url": "/script3"},
        ]
    })

@app.route('/investing.py')
def script1():
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
def script2():
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
        print("Data received:", data) # Log received data
        
        # Here you could use the data to pass to your script if needed
        # For now, just simulate a response
        
        # Example: Call your calculate_irpf.py with the parameters
        # result = subprocess.run(['python3', 'calculate_irpf.py', str(data['quantity'])], capture_output=True, text=True)

        # Simulating a response from your calculate_irpf.py
        output = f"Processed data - Category: {data['category']}, Quantity: {data['quantity']}"
        print("Net Salary back script")
        
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/script2')
# def script2():
#     # Replace with actual script logic
#     result = {"output": "Result of Script 2"}
#     return jsonify(result)

# @app.route('/script3')
# def script3():
#     # Replace with actual script logic
#     result = {"output": "Result of Script 3"}
#     return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

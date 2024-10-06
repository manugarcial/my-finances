from flask import Flask, jsonify
from flask_cors import CORS
import subprocess  # To execute Python scripts

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({
        "scripts": [
            {"name": "Script 1", "url": "/investing.py"}
            # {"name": "Script 2", "url": "/script2"},
            # {"name": "Script 3", "url": "/script3"},
        ]
    })

@app.route('/investing.py')
def script1():
    # Assuming you want to execute a Python script located in the same directory
    try:
        # You can use subprocess to run the script
        result = subprocess.run(['python3', 'investing.py'], capture_output=True, text=True)
        print("Script output:", result.stdout)
        return jsonify({"output": result.stdout})
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

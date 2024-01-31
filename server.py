from flask import Flask, request, jsonify
from flask_cors import CORS
from model import probe_model_5l_profit
import json
import os
app = Flask(__name__)
CORS(app)

# Define route to update data
@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        # Get the uploaded file
        uploaded_file = request.files['file']
        
        # Save the uploaded file as data.json
        uploaded_file.save("data.json")
        
        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define route to get flags
@app.route('/get_flags', methods=['GET'])
def get_flags():
    try:
        if not os.path.exists("data.json"):
            return jsonify({"error": "data.json file not found"}), 404
        else:
            with open("data.json", "r") as file:
                data = json.load(file)
                flags = probe_model_5l_profit(data['data'])['flags']
                return jsonify(flags), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

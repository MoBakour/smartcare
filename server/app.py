import os
import pandas as pd
from flask import Flask, request, jsonify
import sys

# Add packages to path
sys.path.append(os.path.join(os.path.dirname(__file__)))
from wound_monitoring.wound_monitoring import WoundMonitoringPredictor
from wound_healing_prediction.wound_healing_prediction import WoundHealingPredictor

app = Flask(__name__)

# Initialize model variables
infection_predictor = None
healing_predictor = None

def initialize_models():
    global infection_predictor, healing_predictor
    
    try:
        # Initialize infection model
        infection_predictor = WoundMonitoringPredictor()
        if infection_predictor.get_model():
            print("Infection model loaded successfully.")
        else:
            print("Error initializing infection model.")
        
        # Initialize wound healing predictor
        healing_predictor = WoundHealingPredictor()
        if healing_predictor.get_model():
            print("Wound healing model loaded successfully.")
        else:
            print("Error initializing wound healing model.")
    
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        
    return True

@app.route('/predict/infection', methods=['POST'])
def predict_infection():
    global infection_predictor
    
    # Check if the model is initialized
    if infection_predictor is None or infection_predictor.model is None:
        return jsonify({'error': 'Infection model not initialized'}), 500
    
    # Get feature columns from infection_predictor
    feature_columns = infection_predictor.get_feature_columns()
    
    # Get data from request
    try:
        data = request.get_json()
        
        # Ensure all required features are provided
        for feature in feature_columns:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
        
        # Make prediction
        prediction, probability = infection_predictor.predict(data)
        
        if prediction is None:
            return jsonify({'error': 'Error making prediction'}), 500
            
        # Format response
        result = {
            'infection_prediction': 'Yes' if prediction == 1 else 'No',
            'infection_probability': float(probability),
            'input_parameters': data
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/healing', methods=['POST'])
def predict_healing():
    global healing_predictor
    
    # Check if the model is initialized
    if healing_predictor is None or healing_predictor.model is None:
        return jsonify({'error': 'Wound healing model not initialized'}), 500
    
    # Get feature columns from healing_predictor
    feature_columns = healing_predictor.get_feature_columns()
    
    # Get data from request
    try:
        data = request.get_json()
        
        # Ensure all required features are provided
        for feature in feature_columns:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
        
        # Make prediction
        predicted_days = healing_predictor.predict(data)
        
        if predicted_days is None:
            return jsonify({'error': 'Error making prediction'}), 500
        
        # Format response
        result = {
            'healing_time_days': float(predicted_days),
            'input_parameters': data
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Initialize the models before starting the server
    initialize_models()
    
    # Start the Flask server
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
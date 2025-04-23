from flask import Blueprint, request, jsonify
from predictors.wound_monitoring import get_wound_monitoring_predictor
from predictors.wound_healing_prediction import get_wound_healing_predictor
from predictors.treatment_predictor import get_treatment_predictor

prediction_bp = Blueprint('prediction', __name__)

# Initialize model variables
infection_predictor = None
healing_predictor = None
treatment_predictor = None

def initialize_models():
    global infection_predictor, healing_predictor, treatment_predictor
    
    try:
        # Initialize infection model using getter function
        infection_predictor = get_wound_monitoring_predictor()
        if infection_predictor and infection_predictor.model:
            print("Infection model loaded successfully.")
        else:
            print("Error initializing infection model.")
        
        # Initialize wound healing predictor using getter function
        healing_predictor = get_wound_healing_predictor()
        if healing_predictor and healing_predictor.model:
            print("Wound healing model loaded successfully.")
        else:
            print("Error initializing wound healing model.")

        # Initialize treatment predictor using getter function
        treatment_predictor = get_treatment_predictor()
        if treatment_predictor and treatment_predictor.model:
            print("Treatment model loaded successfully.")
        else:
            print("Error initializing treatment model.")
    
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        
    return True

@prediction_bp.route('/infection', methods=['POST'])
def predict_infection():
    global infection_predictor
    
    # Check if the model is initialized
    if infection_predictor is None or infection_predictor.model is None:
        return jsonify({'error': 'Infection model not initialized'}), 500
    
    # Get feature columns from infection_predictor
    prediction_features = infection_predictor.get_prediction_features()
    
    # Get data from request
    try:
        data = request.get_json()
        
        # Ensure all required features are provided
        for feature in prediction_features:
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

@prediction_bp.route('/healing', methods=['POST'])
def predict_healing():
    global healing_predictor
    
    # Check if the model is initialized
    if healing_predictor is None or healing_predictor.model is None:
        return jsonify({'error': 'Wound healing model not initialized'}), 500
    
    # Get feature columns from healing_predictor
    prediction_features = healing_predictor.get_prediction_features()
    
    # Get data from request
    try:
        data = request.get_json()
        
        # Ensure all required features are provided
        for feature in prediction_features:
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

@prediction_bp.route('/treatment', methods=['POST'])
def predict_treatment():
    global treatment_predictor
    
    # Check if the model is initialized
    if treatment_predictor is None or treatment_predictor.model is None:
        return jsonify({'error': 'Treatment model not initialized'}), 500
    
    # Get feature columns from treatment_predictor
    prediction_features = treatment_predictor.get_prediction_features()
    
    # Get data from request
    try:
        data = request.get_json()
        
        # Ensure all required features are provided
        for feature in prediction_features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
        
        # Make prediction
        predicted_treatment, probability = treatment_predictor.predict(data)
        
        if predicted_treatment is None:
            return jsonify({'error': 'Error making prediction'}), 500
        
        # Format response
        result = {
            'predicted_treatment': predicted_treatment,
            'treatment_probability': float(probability),
            'input_parameters': data
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
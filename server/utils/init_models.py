from predictors.wound_monitoring import get_wound_monitoring_predictor
from predictors.wound_healing_prediction import get_wound_healing_predictor

# Initialize model variables
infection_predictor = None
healing_predictor = None

def initialize_models():
    global infection_predictor, healing_predictor
    
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
    
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        
    return True

def predict_infection(data):
    """
    Predict infection probability for given wound data.
    
    Args:
        data (dict): Dictionary containing wound monitoring features
        
    Returns:
        tuple: (prediction, probability) where prediction is 'Yes' or 'No' and probability is float
    """
    global infection_predictor
    
    # Check if the model is initialized
    if infection_predictor is None or infection_predictor.model is None:
        raise Exception('Infection model not initialized')
    
    # Get feature columns from infection_predictor
    prediction_features = infection_predictor.get_prediction_features()
    
    # Ensure all required features are provided
    for feature in prediction_features:
        if feature not in data:
            raise ValueError(f'Missing feature: {feature}')
    
    # Make prediction
    prediction, probability = infection_predictor.predict(data)
    
    if prediction is None:
        raise Exception('Error making prediction')
        
    return ('Yes' if prediction == 1 else 'No', float(probability))

def predict_healing(data):
    """
    Predict healing time for given wound data.
    
    Args:
        data (dict): Dictionary containing wound healing features
        
    Returns:
        float: Predicted healing time in days
    """
    global healing_predictor
    
    # Check if the model is initialized
    if healing_predictor is None or healing_predictor.model is None:
        raise Exception('Wound healing model not initialized')
    
    # Get feature columns from healing_predictor
    prediction_features = healing_predictor.get_prediction_features()
    
    # Ensure all required features are provided
    for feature in prediction_features:
        if feature not in data:
            raise ValueError(f'Missing feature: {feature}')
    
    # Make prediction
    predicted_days = healing_predictor.predict(data)
    
    if predicted_days is None:
        raise Exception('Error making prediction')
    
    return float(predicted_days)
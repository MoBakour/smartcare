# Wound Healing Time Prediction Model
# This model predicts the healing time of wounds based on various features

import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

from predictors.base_predictor import BasePredictor

def get_wound_healing_predictor():
    """Train the model and save it to disk using the BasePredictor
    with custom preprocessing for the wound healing time data
    """
    
    # Initialize the base predictor
    predictor = BasePredictor(
        dataset_name="Synthetic_Wound_Healing_Time_Data.csv",
        model_name="wound_healing",
        numerical_features=['Patient Age', 'Size'],
        categorical_features=['Wound Type', 'Location', 'Severity', 'Infected', 'Treatment'],
        target_feature='Output',
        is_classification=False
    )
    
    # Define the models and parameter grids (same as the original class)
    models = {
        'RandomForest': RandomForestRegressor(random_state=42),
        'GradientBoosting': GradientBoostingRegressor(random_state=42),
        'LinearRegression': LinearRegression()
    }
    
    param_grids = {
        'RandomForest': {
            'model__n_estimators': [50, 100],
            'model__max_depth': [None, 10, 20]
        },
        'GradientBoosting': {
            'model__n_estimators': [50, 100],
            'model__learning_rate': [0.01, 0.1]
        },
        # LinearRegression has no hyperparameters to tune
        'LinearRegression': {}
    }
    
    # If we couldn't load the model, train a new one
    if not predictor.load_model():
        # Load data
        data = predictor.load_data(predictor.dataset_path, 5000)
        if data is None:
            print("Failed to load data.")
            return
        
        # Apply custom preprocessing here if needed
        print("Applying preprocessing to wound healing data...")
        # Example of potential custom preprocessing:
        # data['Custom_Feature'] = data['Feature1'] * data['Feature2']
        
        # Standard preprocessing
        X_train, X_test, y_train, y_test = predictor.preprocess_data(data)
        
        # Train model
        predictor.train_model(X_train, y_train, models, param_grids, scoring_metric='neg_mean_squared_error')
        
        # Evaluate model
        predictor.evaluate_model(X_test, y_test)
        
        # Save model
        try:
            joblib.dump(predictor.model, predictor.model_path)
            joblib.dump(predictor.preprocessor, predictor.preprocessor_path)
            
            print(f"Model saved to {predictor.model_path}")
            print(f"Preprocessor saved to {predictor.preprocessor_path}")
            print("\nModel loaded successfully.")
        except Exception as e:
            print(f"Error saving model: {e}")
            print("Failed to save the model.")
            return
    
    # Example prediction
    example = {
        'Wound Type': 'Burn',
        'Location': 'Arm',
        'Severity': 'Moderate',
        'Infected': 'Yes',
        'Patient Age': 45,
        'Size': 12.5,
        'Treatment': 'Antibiotics (Oral)'
    }
    
    predicted_days = predictor.predict(example)
    if predicted_days is not None:
        print(f"\nExample Prediction:")
        print(f"For a {example['Severity']} {example['Wound Type']} on the {example['Location']}, " + 
              f"{example['Size']} cm², {example['Infected']} infection, {example['Patient Age']} year old patient:")
        print(f"Predicted healing time: {predicted_days:.1f} days")
    
    return predictor
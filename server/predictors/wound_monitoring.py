# Wound Infection Monitoring Model
# This model predicts whether a wound is infected based on various measurements

import os
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

from predictors.base_predictor import BasePredictor

def get_wound_monitoring_predictor():
    """Train the model and save it to disk using the BasePredictor
    with custom preprocessing for the wound monitoring data
    """
    
    # Initialize the base predictor
    predictor = BasePredictor(
        dataset_name="Synthetic_Wound_Healing_Data.csv",
        model_name="wound_monitoring",
        numerical_features=['Wound Temperature', 'Wound pH', 'Moisture Level', 'Drug Release'],
        categorical_features=[],
        target_feature='Infection_Encoded',
        is_classification=True
    )
    
    # Define the models and parameter grids (same as the original class)
    models = {
        'RandomForest': RandomForestClassifier(random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
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
        'LogisticRegression': {
            'model__C': [0.1, 1.0, 10.0]
        }
    }
    
    # If we couldn't load the model, train a new one
    if not predictor.load_model():
        # Load data
        data = predictor.load_data(predictor.dataset_path)
        if data is None:
            print("Failed to load data.")
            return
        
        # Custom preprocessing step for infection encoding
        print("Applying custom preprocessing: encoding Infection feature...")
        data['Infection_Encoded'] = data['Infection'].map({'No': 0, 'Yes': 1})
        
        # Standard preprocessing
        X_train, X_test, y_train, y_test = predictor.preprocess_data(data)
        
        # Train model
        predictor.train_model(X_train, y_train, models, param_grids, scoring_metric='accuracy')
        
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
        'Wound Temperature': 37.8,
        'Wound pH': 6.8,
        'Moisture Level': 75,
        'Drug Release': 15
    }
    
    prediction, probability = predictor.predict(example)
    if prediction is not None:
        print(f"\nExample Prediction:")
        print(f"For wound measurements: {example}")
        print(f"Infection prediction: {'Yes' if prediction == 1 else 'No'}")
        print(f"Infection probability: {probability:.2f}")
    
    return predictor
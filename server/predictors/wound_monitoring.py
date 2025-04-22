# Wound Infection Monitoring Model
# This model predicts whether a wound is infected based on various measurements

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib

class WoundMonitoringPredictor:
    def __init__(self):
        self.dataset_name = "Synthetic_Wound_Healing_Data.csv"
        self.dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets', self.dataset_name)
        self.model = None
        self.preprocessor = None
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'wound_monitoring_model.pkl')
        self.preprocessor_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'wound_monitoring_preprocessor.pkl')
        self.numerical_features = ['Wound Temperature', 'Wound pH', 'Moisture Level', 'Drug Release']
        self.categorical_features = []
        self.prediction_features = self.numerical_features + self.categorical_features
        self.target_feature = 'Infection_Encoded'
    
    def load_data(self, dataset_path, nrows=1000):
        """Load the wound healing dataset"""
        try:
            data = pd.read_csv(dataset_path, nrows=nrows)
            print(f"Data loaded successfully. Shape: {data.shape}")
            print(f"Data columns: {data.columns.tolist()}")
            print(data.head())
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def preprocess_data(self, data):
        """Preprocess the data for model training"""        
        # Encoding categorical features - target is binary (Yes/No)
        data['Infection_Encoded'] = data['Infection'].map({'No': 0, 'Yes': 1})
        
        # Select features and target
        X = data[self.prediction_features]
        y = data[self.target_feature]
        
        # Create preprocessing pipeline
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        # Even though we don't have categorical features now, we're setting up the architecture for future
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine preprocessing steps
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """Train the wound infection prediction model"""
        # Create a pipeline with preprocessing and model
        models = {
            'RandomForest': RandomForestClassifier(random_state=42),
            'GradientBoosting': GradientBoostingClassifier(random_state=42),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        best_model = None
        best_score = float('-inf')
        best_model_name = None
        
        print("Training models...")
        
        # Train and evaluate each model
        for name, model in models.items():
            pipeline = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('model', model)
            ])
            
            # Define parameter grid for GridSearchCV
            if name == 'RandomForest':
                param_grid = {
                    'model__n_estimators': [50, 100],
                    'model__max_depth': [None, 10, 20]
                }
            elif name == 'GradientBoosting':
                param_grid = {
                    'model__n_estimators': [50, 100],
                    'model__learning_rate': [0.01, 0.1]
                }
            else:  # LogisticRegression
                param_grid = {
                    'model__C': [0.1, 1.0, 10.0]
                }
            
            # Use GridSearchCV to find best parameters
            if param_grid:
                grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
                grid_search.fit(X_train, y_train)
                pipeline = grid_search.best_estimator_
                best_params = grid_search.best_params_
                score = grid_search.best_score_
                print(f"{name} best parameters: {best_params}")
            else:
                pipeline.fit(X_train, y_train)
                score = accuracy_score(y_train, pipeline.predict(X_train))
            
            print(f"{name} training accuracy: {score:.4f}")
            
            if best_model is None or score > best_score:
                best_model = pipeline
                best_score = score
                best_model_name = name
        
        print(f"\nBest model: {best_model_name} with accuracy: {best_score:.4f}")
        self.model = best_model
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the model performance on test data"""
        if self.model is None:
            print("Model has not been trained yet")
            return
        
        y_pred = self.model.predict(X_test)
        
        # Calculate evaluation metrics
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return accuracy
    
    def get_model(self):
        """Load saved model and preprocessor from files if they exist, 
        otherwise train and save a new model
        
        Returns:
        bool - True if model is loaded/trained successfully, False otherwise
        """
        # Ensure models directory exists
        models_dir = os.path.dirname(self.model_path)
        os.makedirs(models_dir, exist_ok=True)
        
        # Check if model exists
        if os.path.exists(self.model_path) and os.path.exists(self.preprocessor_path):
            try:
                self.model = joblib.load(self.model_path)
                self.preprocessor = joblib.load(self.preprocessor_path)
                print(f"Model loaded from {self.model_path}")
                print(f"Preprocessor loaded from {self.preprocessor_path}")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Will train a new model instead.")
                # Continue to training below
        
        # If we get here, either the model doesn't exist or loading failed
        data = self.load_data(self.dataset_path)
        if data is None:
            return False
        
        # Preprocess data
        X_train, X_test, y_train, y_test = self.preprocess_data(data)
        
        # Train model
        self.train_model(X_train, y_train)
        
        # Evaluate model
        self.evaluate_model(X_test, y_test)
        
        # Save model
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.preprocessor, self.preprocessor_path)
            
            print(f"Model saved to {self.model_path}")
            print(f"Preprocessor saved to {self.preprocessor_path}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def predict(self, wound_features):
        """Make a prediction for wound infection
        
        Parameters:
        wound_features: dict with keys matching self.prediction_features
        
        Returns:
        prediction: int - 0 (No infection) or 1 (Infection)
        probability: float - Probability of infection
        """
        if self.model is None:
            print("Model has not been trained or loaded yet")
            return None, None
        
        try:
            # Convert input dictionary to DataFrame
            input_df = pd.DataFrame([wound_features])
            
            # Ensure we have all required features
            for feature in self.prediction_features:
                if feature not in input_df.columns:
                    print(f"Missing feature: {feature}")
                    return None, None
            
            # Extract only the relevant features in the correct order
            input_features = input_df[self.prediction_features]
            
            # Make prediction using the pipeline
            prediction = self.model.predict(input_features)[0]
            probability = self.model.predict_proba(input_features)[0][1]  # Probability of class 1 (infected)
            
            return prediction, probability
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None, None
    
    def get_prediction_features(self):
        """Return the feature columns required for prediction"""
        return self.prediction_features

def train_and_save_model():
    """Train the model and save it to disk"""
    predictor = WoundMonitoringPredictor()
    
    # Get or train model
    if not predictor.get_model():
        print("Failed to train and save model!")
        return
    
    print("\nModel training completed!")
    
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

if __name__ == "__main__":
    train_and_save_model()
# Wound Healing Time Prediction Model
# This model predicts the healing time of wounds based on various features

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import joblib

class WoundHealingPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wound_healing_model.pkl')
        self.preprocessor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wound_healing_preprocessor.pkl')
        self.categorical_features = ['Wound Type', 'Location', 'Severity', 'Infected', 'Treatment']
        self.numerical_features = ['Patient Age', 'Size']
        self.feature_columns = self.categorical_features + self.numerical_features
        
    def load_data(self, data_path, nrows=1000):
        """Load the wound healing dataset"""
        try:
            data = pd.read_csv(data_path, nrows=nrows)
            print(f"Data loaded successfully. Shape: {data.shape}")
            print(f"Data columns: {data.columns.tolist()}")
            print(data.head())
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
            
    def preprocess_data(self, data):
        """Preprocess the data for model training"""
        # Separate features and target
        X = data[self.feature_columns]
        y = data['Output']
        
        # Create preprocessing pipeline
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        # Categorical features are one-hot encoded
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine preprocessing steps
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features),
            ])
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """Train the wound healing prediction model"""
        # Create a pipeline with preprocessing and model
        models = {
            'RandomForest': RandomForestRegressor(random_state=42),
            'GradientBoosting': GradientBoostingRegressor(random_state=42),
            'LinearRegression': LinearRegression()
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
            else:  # LinearRegression
                param_grid = {}
            
            # Use GridSearchCV to find best parameters
            if param_grid:
                grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
                grid_search.fit(X_train, y_train)
                pipeline = grid_search.best_estimator_
                best_params = grid_search.best_params_
                score = -grid_search.best_score_  # Convert back to positive MSE
                print(f"{name} best parameters: {best_params}")
            else:
                pipeline.fit(X_train, y_train)
                score = mean_squared_error(y_train, pipeline.predict(X_train))
            
            print(f"{name} training MSE: {score:.4f}")
            
            if best_model is None or score < best_score:
                best_model = pipeline
                best_score = score
                best_model_name = name
        
        print(f"\nBest model: {best_model_name} with MSE: {best_score:.4f}")
        self.model = best_model
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the model performance on test data"""
        if self.model is None:
            print("Model has not been trained yet")
            return
        
        y_pred = self.model.predict(X_test)
        
        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\nModel Evaluation Metrics:")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        return mse, mae, r2
    
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
        datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datasets')
        data_path = os.path.join(datasets_dir, 'Synthetic_Wound_Healing_Time_Data.csv')
        data = self.load_data(data_path)
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
        """Make a prediction for wound healing time
        
        Parameters:
        wound_features: dict with keys:
            - 'Wound Type': str
            - 'Location': str
            - 'Severity': str
            - 'Infected': str
            - 'Patient Age': int
            - 'Size': float
            - 'Treatment': str
        
        Returns:
        predicted_days: float - predicted healing time in days
        """
        if self.model is None:
            print("Model has not been trained or loaded yet")
            return None
        
        try:
            # Convert input dictionary to DataFrame
            input_df = pd.DataFrame([wound_features])
            
            # Ensure we have all required features
            for feature in self.feature_columns:
                if feature not in input_df.columns:
                    print(f"Missing feature: {feature}")
                    return None, None
            
            # Extract only the relevant features in the correct order
            input_features = input_df[self.feature_columns]

            # Make prediction
            prediction = self.model.predict(input_features)[0]

            return prediction
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None
        
    def get_feature_columns(self):
        """Get the feature columns used for training the model"""
        return self.feature_columns

def train_and_save_model():
    """Train the model and save it to disk"""
    predictor = WoundHealingPredictor()
    
    # Get or train model
    if not predictor.get_model():
        print("Failed to train and save model!")
        return
    
    print("\nModel training completed!")
    
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

if __name__ == "__main__":
    train_and_save_model()
# filepath: c:\Users\user\Desktop\SmartCare\server\predictors\base_predictor.py
# Base Predictor class for ML models in SmartCare
# This abstract base class provides common functionality for all predictors

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error, mean_squared_error, mean_absolute_error, r2_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

class BasePredictor:
    def __init__(self, dataset_name, model_name, numerical_features, categorical_features, target_feature, is_classification=True):
        """Initialize the base predictor with common attributes
        
        Parameters:
        dataset_name (str): Name of the dataset file
        model_name (str): Name prefix for the model and preprocessor files
        numerical_features (list): List of numerical feature column names
        categorical_features (list): List of categorical feature column names
        target_feature (str): Name of target column for prediction
        """
        # Dataset info
        self.dataset_name = dataset_name
        self.dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                         'datasets', self.dataset_name)
        
        # Features info
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.prediction_features = self.numerical_features + self.categorical_features
        self.target_feature = target_feature
        self.is_classification = is_classification
        
        # Model info
        self.model = None
        self.preprocessor = None
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'models', f'{model_name}_model.pkl')
        self.preprocessor_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                             'models', f'{model_name}_preprocessor.pkl')
    
    def load_data(self, dataset_path, nrows=1000):
        """Load the dataset from CSV file
        
        Parameters:
        dataset_path (str): Path to the CSV file
        nrows (int): Maximum number of rows to read
        
        Returns:
        pandas.DataFrame: The loaded data, or None if error occurs
        """
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
        """Preprocess data
        
        Returns:
        ColumnTransformer: The preprocessing pipeline
        """
        # Select features and target
        X = data[self.prediction_features]
        y = data[self.target_feature]

        # Create preprocessing pipeline
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine preprocessing steps
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train, models=None, param_grids=None, scoring_metric=None):
        """Train model with grid search for best parameters
        
        Parameters:
        X_train: Features training data
        y_train: Target training data
        models: Dictionary of model names and their instances
        param_grids: Dictionary of model names and their parameter grids for GridSearchCV
        scoring_metric: Metric to use for model selection ('accuracy' for classification, 'neg_mean_squared_error' for regression)
        
        Returns:
        The trained model pipeline
        """
        if models is None or len(models) == 0:
            raise ValueError("No models provided for training")
            
        if param_grids is None:
            param_grids = {}
            
        if scoring_metric is None:
            scoring_metric = 'accuracy' if self.is_classification else 'neg_mean_squared_error'
        
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
            
            # Get parameter grid for this model if available
            param_grid = param_grids.get(name, {})
            
            # Use GridSearchCV to find best parameters if a param grid is provided
            if param_grid:
                grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring=scoring_metric)
                grid_search.fit(X_train, y_train)
                pipeline = grid_search.best_estimator_
                best_params = grid_search.best_params_
                score = grid_search.best_score_
                print(f"{name} best parameters: {best_params}")
            else:
                pipeline.fit(X_train, y_train)
                # For classification models
                if hasattr(pipeline, 'predict_proba') and self.is_classification:
                    score = accuracy_score(y_train, pipeline.predict(X_train))
                # For regression models
                else:
                    predictions = pipeline.predict(X_train)
                    score = -mean_squared_error(y_train, predictions)
            
            # Print appropriate metrics based on model type
            if self.is_classification:
                print(f"{name} training accuracy: {score if score <= 1.0 else -score:.4f}")
            else:
                # For regression, we want to minimize error
                mse = -score if score < 0 else score
                print(f"{name} training MSE: {mse:.4f}")
            
            # For classification, higher score is better; for regression with neg_mse, higher (less negative) is better
            if best_model is None or score > best_score:
                best_model = pipeline
                best_score = score
                best_model_name = name
        
        # Report results depending on task type
        if self.is_classification:
            print(f"\nBest model: {best_model_name} with accuracy: {best_score if best_score <= 1.0 else -best_score:.4f}")
        else:
            mse = -best_score if best_score < 0 else best_score
            print(f"\nBest model: {best_model_name} with MSE: {mse:.4f}")
            
        self.model = best_model
        return self.model

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model performance on test data
        
        Parameters:
        X_test: Features test data
        y_test: Target test data
        
        Returns:
        For classification:
            accuracy: float - The accuracy score
            classification_report: dict - The classification report including precision, recall, f1-score
            confusion_matrix: array - The confusion matrix
        For regression:
            mse: float - Mean Squared Error
            mae: float - Mean Absolute Error
            r2: float - R² Score
        """
        if self.model is None:
            print("Model has not been trained or loaded yet")
            return None
        
        # Make predictions on test data
        y_pred = self.model.predict(X_test)
        
        # Different evaluation metrics for classification vs regression
        if self.is_classification:
            
            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            matrix = confusion_matrix(y_test, y_pred)
            
            # Print results
            print("\nClassification Model Evaluation:")
            print(f"Model Accuracy: {accuracy:.4f}")
            print("Classification Report:")
            print(classification_report(y_test, y_pred))
            print("Confusion Matrix:")
            print(matrix)
            
            # Return metrics
            return accuracy, report, matrix
        else:            
            # Calculate evaluation metrics
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Print results
            print("\nRegression Model Evaluation:")
            print(f"Mean Squared Error: {mse:.4f}")
            print(f"Mean Absolute Error: {mae:.4f}")
            print(f"R² Score: {r2:.4f}")
            
            # Return metrics
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
    
    def predict(self, features):
        """Make a prediction based on input features
        
        Parameters:
        features: dict with keys matching self.prediction_features
        
        Returns:
        For classification:
            prediction: int/string - The predicted class
            probability: float - Probability of the predicted class (or class 1 in binary)
        For regression:
            prediction: float - The predicted value
        """
        if self.model is None:
            print("Model has not been trained or loaded yet")
            return None if not self.is_classification else (None, None)
        
        try:
            # Convert input dictionary to DataFrame
            input_df = pd.DataFrame([features])
            
            # Validate input features
            if not self.validate_input_features(input_df):
                return None if not self.is_classification else (None, None)
            
            # Extract only the relevant features in the correct order
            input_features = input_df[self.prediction_features]
            
            # Make prediction using the pipeline
            prediction = self.model.predict(input_features)[0]
            
            # For classification models, return both prediction and probability
            if self.is_classification:
                # Check if model has predict_proba method (most classifiers do)
                if hasattr(self.model, 'predict_proba'):
                    # Get probability of positive class (index 1 for binary classification)
                    # For multiclass, this would be the probability of the predicted class
                    probabilities = self.model.predict_proba(input_features)[0]
                    
                    # For binary classification, return probability of class 1
                    if len(probabilities) == 2:
                        probability = probabilities[1]
                    else:
                        # For multiclass, get probability of predicted class
                        predicted_class_idx = int(prediction) if isinstance(prediction, (int, float)) else list(self.model.classes_).index(prediction)
                        probability = probabilities[predicted_class_idx]
                        
                    return prediction, probability
                else:
                    # If model doesn't have predict_proba (e.g., SVM without probability=True)
                    # Just return prediction and None for probability
                    return prediction, None
            
            # For regression models, just return the prediction
            return prediction
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None if not self.is_classification else (None, None)
    
    def validate_input_features(self, input_df):
        """Validate that all required features are present
        
        Parameters:
        input_df (pandas.DataFrame): DataFrame containing input features
        
        Returns:
        bool: True if all required features are present, False otherwise
        """
        for feature in self.prediction_features:
            if feature not in input_df.columns:
                print(f"Missing feature: {feature}")
                return False
        return True

    def get_prediction_features(self):
        """Return the feature columns required for prediction"""
        return self.prediction_features



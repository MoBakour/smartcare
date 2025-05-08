from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from routes.prediction_routes import prediction_bp, initialize_models
from routes.auth_routes import auth_bp

load_dotenv()

# init & config flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# init & config flask extensions
jwt = JWTManager(app)
mongo = PyMongo(app)
app.db = mongo.cx[os.environ.get("DB_NAME")]

# register blueprints
app.register_blueprint(prediction_bp, url_prefix="/predict")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# init ai models and start flask server
if __name__ == '__main__':
    initialize_models()
    
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=8080)
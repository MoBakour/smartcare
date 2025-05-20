from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
import os
import google.generativeai as genai
from utils.init_models import initialize_models

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.patient_routes import patient_bp
from routes.prediction_routes import prediction_bp

# load env variables
load_dotenv()

# init & config flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
PORT = int(os.environ.get('PORT')) or 5000

# Configure Google Generative AI
genai.configure(api_key=os.environ.get('GENAI_API_KEY'))

# manage uploads
app.config['UPLOAD_FOLDER'] = "uploads"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# enable cors
CORS(app)

# init & config flask extensions
jwt = JWTManager(app)
mongo = PyMongo(app)
app.db = mongo.cx[os.environ.get("DB_NAME")]

# register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(patient_bp, url_prefix="/patient")
app.register_blueprint(prediction_bp, url_prefix="/predict")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# init ai models and start flask server
if __name__ == '__main__':
    initialize_models()
    
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=PORT)
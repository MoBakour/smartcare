from flask import Flask
from routes.prediction_routes import prediction_bp, initialize_models

app = Flask(__name__)

app.register_blueprint(prediction_bp, url_prefix='/api')

if __name__ == '__main__':
    initialize_models()
    
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
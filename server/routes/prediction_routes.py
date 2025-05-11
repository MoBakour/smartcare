from flask import Blueprint, request, jsonify
from utils.init_models import predict_infection, predict_healing

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/infection', methods=['POST'])
def infection_route():
    try:
        data = request.get_json()
        prediction, probability = predict_infection(data)
        
        # Format response
        result = {
            'infection_prediction': prediction,
            'infection_probability': probability,
            'input_parameters': data
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/healing', methods=['POST'])
def healing_route():
    try:
        data = request.get_json()
        predicted_days = predict_healing(data)
        
        # Format response
        result = {
            'healing_time_days': predicted_days,
            'input_parameters': data
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
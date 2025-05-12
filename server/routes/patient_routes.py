from flask import Blueprint, request, jsonify, current_app as app, send_file, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, UTC
from bson import ObjectId
from marshmallow import ValidationError
from utils.validation import NewPatientSchema
from utils.init_models import predict_healing, predict_infection
from utils.handlers import stream_avatar
import os
import json
import uuid
import csv
import time

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
ALLOWED_SOURCE_EXTENSIONS = {'.csv'}


patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/new", methods=["POST"])
@jwt_required()
def add_patient():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # Handle avatar image upload
        if "avatar" in request.files:
            avatar_file = request.files["avatar"]
            if avatar_file.filename:
                # Validate file is an image
                if not avatar_file.content_type.startswith('image/'):
                    return jsonify({"error": "Avatar must be an image file"}), 400
                    
                ext = os.path.splitext(avatar_file.filename)[1].lower()
                if ext not in ALLOWED_IMAGE_EXTENSIONS:
                    return jsonify({"error": "Invalid image format. Allowed formats: JPG, JPEG, PNG, GIF"}), 400

                avatar_filename = f"{uuid.uuid4()}{ext}"
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
                avatar_file.save(avatar_path)
                data["avatar"] = f"{avatar_filename}"
        else:
            data["avatar"] = ""

        # Process values
        data["supervisor"] = get_jwt_identity()
        data["wound"] = json.loads(data["wound"])
        
        # Validate the input data
        loaded_data = NewPatientSchema().load(data)

        # Add timestamps
        loaded_data["created_at"] = datetime.now(UTC)
        loaded_data["updated_at"] = datetime.now(UTC)

        # Insert the new patient into the database
        result = app.db.patients.insert_one(loaded_data)
        
        # Return the newly created patient 
        data["_id"] = str(result.inserted_id)

        return jsonify({"msg": "Patient created", "patient": data}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Please fill all fields correctly", "details": err.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400



# get all patients
@patient_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_patients():
    try:
        current_user = get_jwt_identity()
        patients = app.db.patients.find({"supervisor": current_user})
        patients = list(patients)

        # Convert ObjectId to string for JSON serialization
        for patient in patients:
            patient["_id"] = str(patient["_id"])
            patient["created_at"] = str(patient["created_at"])
            patient["updated_at"] = str(patient["updated_at"])

        return jsonify({"patients": patients}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



"""
Don't only get patient by id, but also by supervisor id (to make sure not anyone can get any patient data).
Check /delete implementation below to understand what I mean.
"""
# get patient by id
@patient_bp.route("/<string:patient_id>", methods=["GET"])
@jwt_required()
def get_patient(patient_id):
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Check if the patient exists
        patient = app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Convert ObjectId to string for JSON serialization
        patient["_id"] = str(patient["_id"])
        patient["created_at"] = str(patient["created_at"])
        patient["updated_at"] = str(patient["updated_at"])
        
        return jsonify({"patient": patient}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# stream patient avatar
@patient_bp.route("/avatar/<string:patient_id>", methods=["GET"])
def stream_patient_avatar(patient_id):
    return stream_avatar(patient_id, "patients")



"""
Make it possible to upload a csv file into the server.
Rename it to a unique id and save it in the server filesystem somewhere.
Connect it to the user by updating user document in the DB and adding a new field called "source" with the value of the file id.
"""
# Helper function to check allowed file extensions
def allowed_file(filename):
    return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_SOURCE_EXTENSIONS


# connect patient to data source
@patient_bp.route("/connect/<string:patient_id>", methods=["POST"])
@jwt_required()
def connect_patient(patient_id):
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Check if the patient exists
        patient = app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Get the file from the request
        file = request.files["file"]    
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Process the file if it has an allowed extension
        if allowed_file(file.filename):
            filename = f"{patient_id}.csv"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return jsonify({"error": "Invalid file extension"}), 400

        return jsonify({"msg": "Patient connected to data source"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# stream health data
@patient_bp.route("/monitor/<string:patient_id>", methods=["GET"])
def stream_health_data(patient_id):
    try:
        patient = app.db.patients.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], patient_id + ".csv")

        def generate():
            try:
                with open(filepath, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Convert string values to numbers
                        data = {
                            'Time': float(row['Time']),
                            'Wound Temperature': float(row['Wound Temperature']), 
                            'Wound pH': float(row['Wound pH']),
                            'Moisture Level': float(row['Moisture Level']),
                            'Drug Release': float(row['Drug Release']),
                        }

                        patient_data = {
                            'Wound Type': patient['wound']['type'],
                            'Location': patient['wound']['location'],
                            'Severity': patient['wound']['severity'],
                            'Infected': patient['wound']['infected'],
                            'Patient Age': patient['age'],
                            'Size': patient['wound']['size'],
                            'Treatment': patient['wound']['treatment']
                        }

                        # prediction
                        infection = predict_infection(data)
                        total_healing_time = predict_healing(patient_data) # in days
                        
                        # calculate time left based on created_at
                        days_elapsed = (datetime.now(UTC) - patient['created_at'].replace(tzinfo=UTC)).days
                        healing_time_left = max(0, total_healing_time - days_elapsed)

                        # update numeric row
                        data['Infection'] = infection[0]
                        data['Healing Time'] = healing_time_left

                        # Convert row to JSON and send
                        yield f"data: {json.dumps(data)}\n\n"
                        time.sleep(2)
            finally:
                # delete the file after streaming is complete
                try:
                    os.remove(filepath)
                    print(f"Cleaned up file: {filepath}")
                except Exception as e:
                    print(f"Error cleaning up file: {str(e)}")

        return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no'
                }
            )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            




"""
Not a priority now
"""
# update patient data
@patient_bp.route("/update/<string:patient_id>", methods=["PUT"])
@jwt_required()
def update_patient(patient_id):
    pass




# delete patient data
@patient_bp.route("/delete/<string:patient_id>", methods=["DELETE"])
@jwt_required()
def delete_patient(patient_id):
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Check if the patient exists
        patient = app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Delete the patient from the database
        result = app.db.patients.delete_one({"_id": ObjectId(patient_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Failed to delete patient"}), 500
        
        # delete patient avatar from server
        if patient["avatar"]:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"]))

        return jsonify({"msg": "Patient deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete all patients
@patient_bp.route("/deleteall", methods=["DELETE"])
@jwt_required()
def delete_all_patients():
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Get all patients supervised by the current user
        patients = app.db.patients.find({"supervisor": current_user})
        patients = list(patients)

        # Delete all patients supervised by the current user
        app.db.patients.delete_many({"supervisor": current_user})
        
        # delete all patient avatars from server
        for patient in patients:
            if patient["avatar"] and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"])):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"]))

        return jsonify({"msg": "All patients deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    






### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES






# delete all patients globally
@patient_bp.route("/deleteallglobal", methods=["DELETE"])
def delete_all_patients_globally():
    try:
        # Get all patients
        patients = app.db.patients.find({})
        patients = list(patients)

        result = app.db.patients.delete_many({})
        if result.deleted_count == 0:
            return jsonify({"error": "No patients found for deletion"}), 404
        
        # delete all patient avatars from server
        for patient in patients:
            if patient["avatar"]:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"]))

        return jsonify({"msg": "All patients deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



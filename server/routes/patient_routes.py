from flask import Blueprint, request, jsonify, current_app as app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import PyMongoError
import os
from datetime import datetime, UTC
from bson import ObjectId
from marshmallow import Schema, ValidationError, fields, validate
import json
import uuid

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
ALLOWED_SOURCE_EXTENSIONS = {'.csv'}

class WoundSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf([
        "Burn",
        "Puncture",
        "Abrasion",
        "Surgical Wound",
        "Ulcer",
        "Pressure Ulcer",
        "Diabetic Ulcer",
        "Laceration"
    ]))
    location = fields.String(required=True, validate=validate.OneOf([
        "Elbow",
        "Hand",
        "Head",
        "Shoulder",
        "Torso",
        "Knee",
        "Foot",
        "Back",
        "Arm",
        "Leg"
    ]))
    severity = fields.String(required=True, validate=validate.OneOf([
        "Moderate",
        "Mild",
        "Severe"
    ]))
    infected = fields.String(required=True, validate=validate.OneOf(["true", "false"]))
    size = fields.Float(required=True, as_string=True)
    treatment = fields.String(required=True, validate=validate.OneOf([
        "Surgical Debridement",
        "Antibiotics (Oral)",
        "Moist Wound Dressing",
        "Negative Pressure Wound Therapy",
        "Cleaning and Bandage",
        "No Treatment (for mild cases)",
        "Antibiotics (Topical)"
    ]))

class NewPatientSchema(Schema):
    supervisor = fields.String(required=True, validate=validate.Length(min=1))
    name = fields.String(required=True, validate=validate.Length(min=1))
    avatar = fields.String()
    gender = fields.String(required=True, validate=validate.OneOf([
        "male",
        "female"]))
    age = fields.Int(required=True, as_string=True)
    bed = fields.Int(required=True, as_string=True)
    department = fields.String(required=True, validate=validate.Length(min=1))
    blood_type = fields.String(required=True, validate=validate.Length(min=1))
    wound = fields.Nested(WoundSchema, required=True)

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
        loaded_data["wound"]["infected"] = loaded_data["wound"]["infected"] == "true"
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
    try:
        # Check if the patient exists
        patient = app.db.patients.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        
        # Get the avatar file path
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"])

        # Get file extension from avatar filename
        extension = patient["avatar"].split('.')[-1].lower()
        
        # Map common image extensions to MIME types
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg', 
            'png': 'image/png',
            'gif': 'image/gif',
        }
        
        # Get correct MIME type or default to jpeg
        mime_type = mime_types.get(extension, 'image/jpeg')

        # Stream the avatar file with correct MIME type
        return send_file(avatar_path, mimetype=mime_type)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500





"""
Make it possible to upload a csv file into the server.
Rename it to a unique id and save it in the server filesystem somewhere.
Connect it to the user by updating user document in the DB and adding a new field called "source" with the value of the file id.
"""
# Helper function to check allowed file extensions
def allowed_file(filename):
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
            # Generate a unique filename
            filename = f"{patient_id}.csv"
            # Construct the full path where the file will be saved
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the filesystem
            file.save(filepath)
            # Update the patient document with the file id
            app.db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": {"source": filename}}
            )
        else:
            return jsonify({"error": "Invalid file extension"}), 400

        return jsonify({"message": "Patient connected to data source"}), 200
    
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

        return jsonify({"message": "Patient deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500





# delete all patients
@patient_bp.route("/deleteall", methods=["DELETE"])
@jwt_required()
def delete_all_patients():
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Delete all patients supervised by the current user
        result = request.app.db.patients.delete_many({"supervisor": current_user})
        if result.deleted_count == 0:
            return jsonify({"error": "No patients found for deletion"}), 404

        return jsonify({"message": "All patients deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
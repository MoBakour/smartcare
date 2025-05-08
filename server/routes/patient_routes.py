from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError
import os
from werkzeug.utils import secure_filename
from datetime import datetime, UTC
from bson import ObjectId
from marshmallow import Schema, ValidationError, fields, validate


class NewPatientSchema(Schema):
    supervisor = fields.String(required=True)
    name = fields.String(required=True)
    gender = fields.String(required=True, validate=validate.OneOf([
        "male",
        "female"]))
    age = fields.Int(required=True)
    bed = fields.String(required=True)
    department = fields.String(required=True)
    wound_type = fields.String(required=True, validate=validate.OneOf([
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
    infected = fields.Boolean(required=True)
    size = fields.Float(required=True)
    treatment = fields.String(required=True, validate=validate.OneOf([
        "Surgical Debridement",
        "Antibiotics (Oral)",
        "Moist Wound Dressing",
        "Negative Pressure Wound Therapy",
        "Cleaning and Bandage",
        "No Treatment (for mild cases)",
        "Antibiotics (Topical)"
    ]))
    created_at = fields.DateTime(default=datetime.now(UTC))
    updated_at = fields.DateTime(default=datetime.now(UTC))

patient_bp = Blueprint("patient", __name__)

"""
Patient Object:
{
    "supervisor": <string>,     # user id of the current authenticated user. Get it from get_jwt_identity()
    "name": <string>,
    "gender": <string>,
    "age": <int>,
    "bed": <string>,
    "department": <string>,
    "wound_type": <string>,
    "location": <string>,
    "severity": <string>,
    "infected": <boolean>,
    "size": <float>,
    "treatment": <string>,
    "created_at": <datetime>,   # use datetime.now(UTC) to get the current time in UTC
    "updated_at": <datetime>,   # use datetime.now(UTC) to get the current time in UTC
}
You will recieve all above fields from the request body EXCEPT FOR supervisor, created_at and updated_at.

Validation:
Regarding validation, we may look for some package similar to yup/zod to do this.

Validate for possible patient.gender values:
[
    "Male",
    "Female"
]

Validate for possible patient.wound_type values:
[
  "Burn",
  "Puncture",
  "Abrasion",
  "Surgical Wound",
  "Ulcer",
  "Pressure Ulcer",
  "Diabetic Ulcer",
  "Laceration"
]

Validate for possible patient.location values:
[
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
]

Validate for possible patient.severity values:
[
  "Moderate",
  "Mild",
  "Severe"
]

Validate for possible patient.treatment values:
[
  "Surgical Debridement",
  "Antibiotics (Oral)",
  "Moist Wound Dressing",
  "Negative Pressure Wound Therapy",
  "Cleaning and Bandage",
  "No Treatment (for mild cases)",
  "Antibiotics (Topical)"
]
"""
@patient_bp.route("/new", methods=["POST"])
@jwt_required()
def add_patient():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Invalid input"}), 400

        data["supervisor"] = get_jwt_identity()
        data["created_at"] = datetime.now(UTC)
        data["updated_at"] = datetime.now(UTC)

        # Validate the input data
        loaded_data = NewPatientSchema().load(data)

        # Insert the new patient into the database
        result = request.app.db.patients.insert_one(loaded_data)
        
        # Return the newly created patient 
        data["_id"] = str(result.inserted_id)

        return jsonify({"msg": "Patient created", "patient": data}), 201
    
    except ValidationError as err:
        print("Validation Errors:", err.messages)
    
    except PyMongoError as e:
        print("Database Error:", e)
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400


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
        patient = request.app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Convert ObjectId to string for JSON serialization
        patient["_id"] = str(patient["_id"])
        patient["created_at"] = str(patient["created_at"])
        patient["updated_at"] = str(patient["updated_at"])
        
        return jsonify({"patient": patient}), 200
    

    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500



"""
Make it possible to upload a csv file into the server.
Rename it to a unique id and save it in the server filesystem somewhere.
Connect it to the user by updating user document in the DB and adding a new field called "source" with the value of the file id.
"""


# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'patient_data'
# Define allowed extensions (optional but good practice)
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# connect patient to data source
@patient_bp.route("/connect/<string:patient_id>", methods=["POST"])
@jwt_required()
def connect_patient(patient_id):
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Check if the patient exists
        patient = request.app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
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
            request.app.db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": {"source": filename}}
            )
        else:
            return jsonify({"error": "Invalid file extension"}), 400

        return jsonify({"message": "Patient connected to data source"}), 200
    
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500





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
        patient = request.app.db.patients.find_one({"_id": ObjectId(patient_id), "supervisor": current_user})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Delete the patient from the database
        result = request.app.db.patients.delete_one({"_id": ObjectId(patient_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Failed to delete patient"}), 500

        return jsonify({"message": "Patient deleted successfully"}), 200

    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500





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

    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
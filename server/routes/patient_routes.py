from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError
from datetime import datetime, UTC
from bson import ObjectId

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

Vadliate for possible patient.gender values:
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
    pass





"""
Don't only get patient by id, but also by supervisor id (to make sure not anyone can get any patient data).
Check /delete implementation below to understand what I mean.
"""
# get patient by id
@patient_bp.route("/<string:patient_id>", methods=["GET"])
@jwt_required()
def get_patient(patient_id):
    pass




"""
Make it possible to upload a csv file into the server.
Rename it to a unique id and save it in the server filesystem somewhere.
Connect it to the user by updating user document in the DB and adding a new field called "source" with the value of the file id.
"""
# connect patient to data source
@patient_bp.route("/connect/<string:patient_id>", methods=["POST"])
@jwt_required()
def connect_patient(patient_id):
    pass




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
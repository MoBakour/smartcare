from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.security import generate_password_hash
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, UTC
from bson import ObjectId
from utils.handlers import stream_avatar
from utils.validation import validate_signup, ValidationError
import os
import uuid

# initialize blueprint
user_bp = Blueprint("user", __name__)

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

# get current user
@user_bp.route("/get", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        # get current user from JWT token
        current_user = get_jwt_identity()

        # find user in db
        user = app.db.users.find_one({"_id": ObjectId(current_user)})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # preprocess
        user.pop("password", None)
        user["_id"] = str(user["_id"])

        return jsonify({"user": user}), 200

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# stream user avatar
@user_bp.route("/avatar/<string:id>", methods=["GET"])
def stream_user_avatar(id):
    return stream_avatar(id, "users")

@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        current_user = get_jwt_identity()
        user = app.db.users.find_one_and_delete({"_id": ObjectId(current_user)})

        # delete all patient data
        patients = app.db.patients.find({"supervisor": current_user})
        patients = list(patients)
        app.db.patients.delete_many({"supervisor": current_user})

        # delete all patients avatars
        for patient in patients:
            if "avatar" in patient and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"])):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], patient["avatar"]))

        # delete account avatar
        if "avatar" in user and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], user["avatar"])):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user["avatar"]))

        return jsonify({"msg": "User deleted"}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500



@user_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        data = request.form.to_dict()
        current_user = get_jwt_identity()

        # get user
        user = app.db.users.find_one({"_id": ObjectId(current_user)})

        # validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # validate email uniqueness
        if data.get("email") != user.get("email"):
            if app.db.users.find_one({"email": data.get("email")}):
                return jsonify({"error": "Email already in use"}), 400
        
        validate_signup({
            "username": data.get("username"),
            "email": data.get("email"),
            "password": None if data.get("password") == "" else data.get("password"),
        }, optional=["password"])

        updates = {
            "username": data.get("username"),
            "email": data.get("email"),
            "updated_at": datetime.now(UTC)
        }
        
        if data["password"] != "":
            updates["password"] = generate_password_hash(data.get("password"))

        # upload avatar
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
                updates["avatar"] = f"{avatar_filename}"

            # delete old avatar
            if "avatar" in user and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], user["avatar"])):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user["avatar"]))

        updated_doc = app.db.users.find_one_and_update(
            {"_id": ObjectId(current_user)},                   
            {"$set": updates},      
            return_document=ReturnDocument.AFTER        
        )

        # preprocess
        updated_doc.pop("password", None)
        updated_doc["_id"] = str(updated_doc["_id"])
        
        return jsonify({"user": updated_doc}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except ValidationError as e:
        return jsonify({"error": e.message}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500




### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES
### INTERNAL TOOL  -  TESTING AND DEVELOPMENT ROUTES




"""
This route is for testing purpose only.
It should be removed or limited to admin access in production.
"""   
@user_bp.route("/deleteallglobal", methods=["DELETE"])
def delete_all_users():
    try:
        app.db.users.delete_many({})
        return jsonify({"msg": "All users deleted"}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

@user_bp.route("/delete/<string:user_email>", methods=["DELETE"])
def delete_user_by_email(user_email):
    try:
        app.db.users.delete_one({"email": user_email})
        return jsonify({"msg": "User deleted"}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# list all users
@user_bp.route("/list", methods=["GET"])
def list_users():
    try:
        users = app.db.users.find()
        users = list(users)

        for user in users:
            user.pop("password", None)
            patients = app.db.patients.find({"supervisor": str(user["_id"])})
            patients = list(patients)
            user["patients"] = patients

        return jsonify({"users": list(users)}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500



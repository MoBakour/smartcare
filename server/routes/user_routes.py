from flask import Blueprint, jsonify, current_app as app
from pymongo.errors import PyMongoError
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

# initialize blueprint
user_bp = Blueprint("user", __name__)


# get current user
@user_bp.route("/get", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        # get current user from JWT token
        current_user = get_jwt_identity()

        print(f"Current user ID: {current_user}")

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


@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        current_user = get_jwt_identity()
        app.db.users.delete_one({"_id": ObjectId(current_user)})
        return jsonify({"msg": "User deleted"}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
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



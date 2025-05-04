from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError
from datetime import datetime, UTC
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ("username", "email", "password")):
            return jsonify({"msg": "Invalid input"}), 400

        # check if user email already exists
        if app.db.users.find_one({"email": data["email"]}):
            return jsonify({"msg": "Email already exists"}), 400

        # hash password
        hashed_password = generate_password_hash(data["password"])

        # create user in db
        doc = {
            "username": data["username"],
            "email": data["email"],
            "password": hashed_password,
            "created_at": str(datetime.now(UTC)),
            "updated_at": str(datetime.now(UTC)),
        }

        user = app.db.users.insert_one(doc)

        # create JWT token
        access_token = create_access_token(identity=str(user.inserted_id))

        # preprocess
        doc.pop("password", None)
        doc["_id"] = str(user.inserted_id)

        return jsonify({"msg": "User created", "user": doc, "access_token": access_token}), 201

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"msg": "An unexpected error occurred"}), 500





@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ("email", "password")):
            return jsonify({"msg": "Invalid input"}), 400

        # find user in db
        user = app.db.users.find_one({
            "email": data["email"]
        })

        if not user:
            return jsonify({"msg": "Incorrect email"}), 404

        # check password
        if not check_password_hash(user["password"], data["password"]):
            return jsonify({"msg": "Incorrect password"}), 401

        # create JWT token
        access_token = create_access_token(identity=str(user["_id"]))

        # preprocess
        user.pop("password", None)
        user["_id"] = str(user["_id"])

        return jsonify({"msg": "Login successful", "user": user, "access_token": access_token}), 200

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"msg": "An unexpected error occurred"}), 500





@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        # get current user from JWT token
        current_user = get_jwt_identity()

        print(f"Current user ID: {current_user}")

        # find user in db
        user = app.db.users.find_one({"_id": ObjectId(current_user)})

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # preprocess
        user.pop("password", None)
        user["_id"] = str(user["_id"])

        return jsonify({"user": user}), 200

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"msg": "An unexpected error occurred"}), 500





"""
This route is for testing purpose only.
It should be removed or limited to admin access in production.
"""   
@auth_bp.route("/deleteall", methods=["DELETE"])
def delete_all_users():
    try:
        app.db.users.delete_many({})
        return jsonify({"msg": "All users deleted"}), 200
    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"msg": "An unexpected error occurred"}), 500
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError
from datetime import datetime, UTC
from utils.validation import validate_signup, validate_login, ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ("username", "email", "password")):
            return jsonify({"error": "Invalid input"}), 400

        # check if user email already exists
        if app.db.users.find_one({"email": data["email"]}):
            return jsonify({"error": "Email already exists"}), 400

        # validate input data
        validate_signup(data)

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
        token = create_access_token(identity=str(user.inserted_id))

        # preprocess
        doc.pop("password", None)
        doc["_id"] = str(user.inserted_id)

        return jsonify({"msg": "User created", "user": doc, "token": token}), 201

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except ValidationError as e:
        app.logger.error(f"Validation error: {e.message}")
        return jsonify({"error": e.message}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500





@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid input"}), 400
        
        # validate input data
        validate_login(data)

        # find user in db
        user = app.db.users.find_one({
            "email": data["email"]
        })

        if not user:
            return jsonify({"error": "Incorrect email"}), 404

        # check password
        if not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Incorrect password"}), 401

        # create JWT token
        token = create_access_token(identity=str(user["_id"]))

        # preprocess
        user.pop("password", None)
        user["_id"] = str(user["_id"])

        return jsonify({"msg": "Login successful", "user": user, "token": token}), 200

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except ValidationError as e:
        app.logger.error(f"Validation error: {e.message}")
        return jsonify({"error": e.message}), 400
    except Exception as e:        
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500



from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ("username", "email", "password")):
            return jsonify({"msg": "Invalid input"}), 400

        # verify uniqueness of username and email
        if app.db.users.find_one({"username": data["username"]}):
            return jsonify({"msg": "Username already exists"}), 400

        if app.db.users.find_one({"email": data["email"]}):
            return jsonify({"msg": "Email already exists"}), 400

        # hash password
        hashed_password = generate_password_hash(data["password"])

        # create user in db
        app.db.users.insert_one({
            "username": data["username"],
            "email": data["email"],
            "password": hashed_password
        })

        # create JWT token
        access_token = create_access_token(identity=data["username"])

        return jsonify({"msg": "User created", "access_token": access_token}), 201

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

        if not data or not all(key in data for key in ("username", "password")):
            return jsonify({"msg": "Invalid input"}), 400

        # find user in db
        user = app.db.users.find_one({
            "$or": [{"username": data["username"]}, {"email": data["username"]}]
        })

        if not user:
            return jsonify({"msg": "Incorrect username or email"}), 404

        # check password
        if not check_password_hash(user["password"], data["password"]):
            return jsonify({"msg": "Incorrect password"}), 401

        # create JWT token
        access_token = create_access_token(identity=user["username"])

        return jsonify({"msg": "Login successful", "access_token": access_token}), 200

    except PyMongoError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"msg": "An unexpected error occurred"}), 500
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)

from flask_server.controllers.auth import AuthController

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    # Ensure all fields are present
    if not all(key in body for key in ("username", "password")):
        return jsonify(message="Missing required fields"), 400

    username = body["username"]
    password = body["password"]

    result = AuthController.login(username, password)

    if result["status"] == False:
        return (
            jsonify(
                user=None,
                message=result["message"],
            ),
            result["status_code"],
        )

    response = jsonify(
        user=result["user"],
        message="User logged in successfully.",
    )

    access_token = create_access_token(identity=result["user"])
    set_access_cookies(response, access_token)

    return (
        response,
        201,
    )


@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify(message="User logged out successfully.")
    unset_jwt_cookies(response)
    return response, 200


@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@auth.route("/register", methods=["POST"])
def register():
    body = request.get_json()

    # Ensure all fields are present
    if not all(key in body for key in ("username", "password", "email")):
        return jsonify(message="Missing required fields"), 400

    username = body["username"]
    password = body["password"]
    email = body["email"]

    result = AuthController.register(username, password, email)

    if result["status"] == False:
        return (
            jsonify(
                user=None,
                message=result["message"],
            ),
            result["status_code"],
        )

    return (
        jsonify(user=result["user"], message="New user registered successfully."),
        201,
    )

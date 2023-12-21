from flask import Blueprint, jsonify, request

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

    return (
        jsonify(user=result["user"], message="User logged in successfully."),
        201,
    )


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

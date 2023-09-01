from flask import Blueprint, jsonify, request

from flask_server.controllers.user import UserController

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def register():
    body = request.get_json()

    # Ensure all fields are present
    if not all(key in body for key in ("username", "password", "email")):
        return jsonify(message="Missing required fields"), 400

    username = body["username"]
    password = body["password"]
    email = body["email"]

    result = UserController.create(username, password, email)

    if result["status"] == False:
        return (
            jsonify(
                status=result["status"],
                user=None,
                status_code=result["status_code"],
                message=result["message"],
            ),
            result["status_code"],
        )

    return (
        jsonify(user=result["user"], message="New user registered successfully."),
        201,
    )

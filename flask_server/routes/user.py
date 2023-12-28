from flask import Blueprint, jsonify, request

from flask_server.controllers.user import UserController
from flask_server.decorators import jwt_or_api_key_required

user = Blueprint("user", __name__, url_prefix="/user")


# TODO: Clean up routes
@user.route("/update", methods=["POST"])
@jwt_or_api_key_required()
def update_users():
    body = request.get_json()

    username = body["username"]
    updates = body["updates"]

    if UserController.update_user(username, updates):
        return jsonify(message=f"User {username} updated"), 201

    return jsonify(message=f"There was an issue updating {username}"), 500

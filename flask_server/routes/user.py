from flask import Blueprint, jsonify, request

from flask_server.controllers.user import UserController

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/all", methods=["GET"])
def all_users():
    users = UserController.get_all()

    return jsonify(users=users)


@user.route("/delete-all", methods=["DELETE"])
def delete_all_users():
    UserController.delete_all()

    return jsonify(message="deleted successfully")

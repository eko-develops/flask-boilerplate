from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request

from flask_server.controllers.auth import AuthController


def jwt_or_api_key_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                print("Verified JWT in request")
            except Exception as e:
                api_key = request.headers.get("API-KEY")

                result = AuthController.check_api_key(api_key)
                if result is False:
                    return jsonify(message="Missing/invalid JWT or API Key"), 401
                print("Verified API Key in request")

            return fn(*args, **kwargs)

        return decorator

    return wrapper

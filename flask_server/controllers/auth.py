from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

from sqlalchemy.exc import IntegrityError

from flask_server.extensions import ph, db
from flask_server.controllers.user import UserController
from flask_server.models.user import User


class AuthController:
    @staticmethod
    def login(username, password):
        try:
            user = db.session.execute(
                db.select(User).filter_by(username=username)
            ).scalar_one()

            ph.verify(
                user.password, password
            )  # throws an error if password is not verified

            if ph.check_needs_rehash(user.password):
                UserController.rehash_user_password(user, password)

            return {
                "status": True,
                "user": {"username": user.username, "email": user.email},
            }
        except InvalidHashError as ihe:
            print(ihe)
            return {
                "status": False,
                "status_code": 400,
                "message": "Hash so clearly not valid for login.",
            }
        except VerifyMismatchError as vme:
            print(vme)
            return {
                "status": False,
                "status_code": 400,
                "message": "Hash not valid for password.",
            }
        except VerificationError as ve:
            print(ve)
            return {
                "status": False,
                "status_code": 400,
                "message": "Login verification failed.",
            }
        except Exception as e:
            print(e)
            return {
                "status": False,
                "status_code": 500,
                "message": "An error occured during login.",
            }

    @staticmethod
    def register(username, password, email):
        try:
            hashed_password = ph.hash(password)
            user = User(username=username, password=hashed_password, email=email)
            db.session.add(user)
            db.session.commit()

            return {"status": True, "user": {"username": username, "email": email}}
        except IntegrityError as ie:
            db.session.rollback()
            print(ie)
            return {
                "status": False,
                "status_code": 400,
                "message": "Username or email already exists.",
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "status": False,
                "status_code": 500,
                "message": "An error occured during registration.",
            }

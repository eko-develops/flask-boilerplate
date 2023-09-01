from flask_server.extensions import db, ph
from flask_server.models import User
from sqlalchemy.exc import IntegrityError


class UserController:
    @staticmethod
    def create(username, password, email):
        hashed_password = ph.hash(password)

        try:
            user = User(username=username, password=hashed_password, email=email)
            db.session.add(user)
            db.session.commit()

            return {"status": True, "user": {"username": username, "email": email}}
        except IntegrityError as ie:
            db.session.rollback()
            print(ie)
            # Handle error logging
            return {
                "status": False,
                "status_code": 400,
                "message": "Username or email already exists.",
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            # Handle error logging
            return {
                "status": False,
                "status_code": 500,
                "message": "An error occured during registration.",
            }

    @staticmethod
    def get_all():
        users = db.session.execute(db.select(User)).scalars()
        user_list = []

        for user in users:
            username = user.username
            password = user.password
            email = user.email

            user_list.append([username, password, email])

        return user_list

    @staticmethod
    def delete_all():
        try:
            db.session.query(User).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return str(e)

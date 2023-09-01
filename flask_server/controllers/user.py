from flask_server.extensions import db
from flask_server.models import User
from sqlalchemy.exc import IntegrityError


class UserController:
    @staticmethod
    def register(username, password, email):
        try:
            user = User(username=username, password=password, email=email)
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
        print(users)
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

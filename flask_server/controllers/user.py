from flask_server.extensions import db, ph
from flask_server.models import User


class UserController:
    @staticmethod
    def get_user(username):
        try:
            user = db.session.execute(
                db.select(User).filter_by(username=username)
            ).scalar_one()

            return user
        except Exception as e:
            print(e)

    @staticmethod
    def update_user(username, updates):
        try:
            user = db.session.execute(
                db.select(User).filter_by(username=username)
            ).scalar_one()

            for key, values in updates.items():
                setattr(user, key, values)

            db.session.commit()

            return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def rehash_user_password(user, password):
        try:
            user.password = ph.hash(password)
            db.session.commit()
        except Exception as e:
            print(e)

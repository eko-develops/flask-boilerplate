from flask import Flask

from flask_server.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    
    # Configs
    app.config.from_prefixed_env()

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Models
    from flask_server.models import User

    return app


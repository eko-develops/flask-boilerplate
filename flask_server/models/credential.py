from flask_server.extensions import db


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), unique=True, nullable=False)
    api_key = db.Column(db.String(50), nullable=False)

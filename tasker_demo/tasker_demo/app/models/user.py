from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    oauth_provider = db.Column(db.String(50))
    oauth_sub = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(5),nullable=False)   # user or admin
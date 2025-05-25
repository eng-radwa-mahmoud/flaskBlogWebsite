from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime
from flask_login import UserMixin


class Post(UserMixin, db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(20), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

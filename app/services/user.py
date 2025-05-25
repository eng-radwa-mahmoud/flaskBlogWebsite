from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import uuid
from app.models.user import User
from app.models.author import Author
from app.services.author import AuthorService
import loadmanager

class UserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_by_id(self, id):
        return User.query.get(int(id))

    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def login(self, username, password):
        user = self.get_by_username(username)

        if not user or not check_password_hash(user.password, password):
            return False
        
        loadmanager.load = 1
        login_user(user)

        return True
    
    

    def signup(self, name, username, password):
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            username=username,
            password=generate_password_hash(password),
            role = "user"
        )
        self.db.session.add(user)
        self.db.session.commit()

    def logout(self):
        logout_user()

    def promote(self,user):
        user.role = "admin"
        self.db.session.commit()

    def delete(self, user):
        self.db.session.delete(user)
        self.db.session.commit()



from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
import uuid
from app.models.author import Author
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import loadmanager

class AuthorService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return Author.query.all()
    
    def get_by_username(self, username):
        return Author.query.filter_by(username=username).first()

    def get_by_id(self, id):
        return Author.query.get(int(id))

    def login(self, username, password):
        author = self.get_by_username(username)

        if not author or not check_password_hash(author.password, password):
            return False

        print(author.username)
        loadmanager.load = 2
        login_user(author)

        return True
    
    def logout(self):
        logout_user()
    


    def create(self, name, username, password):
        print("1llllll")
        author = Author(public_id=str(uuid.uuid4()), name=name, username=username, password=password,role="author")
        self.db.session.add(author)
        self.db.session.commit()

    def get_by_public_id(self, public_id):
        return Author.query.filter_by(public_id=public_id).first()

    def update(self, author, name):
        author.name = name
        self.db.session.commit()

    def delete(self, author):
        self.db.session.delete(author)
        self.db.session.commit()


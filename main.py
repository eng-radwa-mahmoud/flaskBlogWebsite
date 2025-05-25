from app import create_app, db, login_manager
from flask_injector import FlaskInjector, singleton
from app.services.posts import Postservice
from app.services.user import UserService
from app.services.author import AuthorService
from app.models.user import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import loadmanager

app = create_app()

# Configure and enable Dependency Injection
def configure(binder):
    binder.bind(Postservice, to=Postservice(db), scope=singleton)
    binder.bind(UserService, to=UserService(db), scope=singleton)
    binder.bind(AuthorService, to=AuthorService(db), scope=singleton)

FlaskInjector(app=app, modules=[configure])

@login_manager.user_loader
def load_user(user_id):

    if loadmanager.load == 1:
        return UserService(db).get_by_id(user_id)
    else:
        return AuthorService(db).get_by_id(user_id)



if __name__ == '__main__':
    app.run()
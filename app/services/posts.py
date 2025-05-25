from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
import uuid
from app.models.post import Post


class Postservice:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return Post.query.all()

    def create(self, title, content, id):
        post = Post(public_id=str(uuid.uuid4()), title=title,  content=content, author_id =id)
        self.db.session.add(post)
        self.db.session.commit()

    def get_by_public_id(self, public_id):
        return Post.query.filter_by(public_id=public_id).first()

    def update(self, post, title,  content):
        post.title = title
        post.content = content
        self.db.session.commit()

    def delete(self, post):
        self.db.session.delete(post)
        self.db.session.commit()


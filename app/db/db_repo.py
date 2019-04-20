import hashlib
from app.db.database import db
from app.db.models import *

from flask_sqlalchemy import SQLAlchemy


class DatabaseRepo:
    def __init__(self, db_sqlalchemy: SQLAlchemy):
        self.db = db_sqlalchemy

    def create_user(self, login: str, password: str, email='', balance_initial: float = 0):
        user = User(login=login, passhash=self._hash_password(password), balance=balance_initial, email=email)
        user.roles.append(Role(name='player'))
        self.db.session.add(user)
        self.db.session.commit()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_all_users(self):
        return User.query.all()

    def create_draw(self, draw_name, events: [Event]):
        pass

    @staticmethod
    def _hash_password(password):
        return hashlib.sha3_256(password.encode('utf-8')).hexdigest()


database_repo = DatabaseRepo(db)

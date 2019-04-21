import hashlib

from sqlalchemy.sql import ClauseElement

from app.db.database import db
from app.db.models import *

from flask_sqlalchemy import SQLAlchemy


class DatabaseRepo:
    def __init__(self, db_sqlalchemy: SQLAlchemy):
        self.db = db_sqlalchemy

    def create_user(self, login: str, password: str, email='', balance_initial: float = 0, is_admin=False):
        user = User(login=login, passhash=self._hash_password(password), balance=balance_initial, email=email)
        user.roles.append(self._get_or_create(db.session, Role, name='player'))
        if is_admin:
            user.roles.append(self._get_or_create(db.session, Role, name='admin'))
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_all_users(self):
        return User.query.all()

    def create_draw(self, draw_name, events: [Event]):
        pass

    @staticmethod
    def _hash_password(password):
        return hashlib.sha3_256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _get_or_create(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance


database_repo = DatabaseRepo(db)

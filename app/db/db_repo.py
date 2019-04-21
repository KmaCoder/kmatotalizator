from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

from app.db.models import *


class DatabaseRepo:

    def __init__(self):
        self.db: SQLAlchemy = None
        self.user_manager: UserManager = None

    def init_db(self, db_sqlalchemy: SQLAlchemy, user_manager: UserManager):
        self.db = db_sqlalchemy
        self.user_manager = user_manager

    def create_user(self, username: str, password: str, email='', balance_initial: float = 0, is_admin=False):
        user = User(username=username,
                    email=email,
                    password=self.user_manager.password_manager.hash_password(password),
                    balance=balance_initial)
        user.roles.append(self._get_or_create(Role, name='player'))
        if is_admin:
            user.roles.append(self._get_or_create(Role, name='admin'))
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_all_users(self):
        return User.query.all()

    def create_draw(self, draw_name, events: [Event]):
        pass

    def _get_or_create(self, model, **kwargs):
        instance = self.db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.db.session.add(instance)
            self.db.session.commit()
            return instance


database_repo = DatabaseRepo()

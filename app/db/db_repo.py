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

    def create_user(self, username: str, password: str, balance_initial: float = 0, is_admin=False) -> User:
        user = User(username=username,
                    password=self.user_manager.password_manager.hash_password(password),
                    balance=balance_initial)
        if is_admin:
            user.roles.append(self._get_or_create(Role, name='admin'))
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_user_by_id(self, user_id) -> User:
        return User.query.get(user_id)

    def get_user_by_username(self, username) -> User:
        return User.query.filter_by(username=username).first()

    def get_all_users(self):
        return User.query.all()

    def update_user_balance(self, user: User, delta: int):
        user.balance = user.balance + delta
        self.db.session.commit()

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

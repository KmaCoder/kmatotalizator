import hashlib
from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    def __int__(self):
        super()

    def create_user(self, login: str, password: str, balance_initial: float = 0):
        from db.models import User
        user = User(login, self._hash_password(password), balance_initial)
        self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        from db.models import User
        return User.query.all()

    @staticmethod
    def _hash_password(password):
        return hashlib.sha3_256(password.encode('utf-8')).hexdigest()


db = Database()

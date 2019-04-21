import datetime
from app.db.database import db

__all__ = ['User', 'Outcome', 'Draw', 'Event', 'Parlay', 'ParlayDetails', 'UserRoles', 'Role']


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class User(BaseModel, db.Model):
    __tablename__ = 'user'

    login = db.Column('login', db.String(50), primary_key=True)
    passhash = db.Column('passhash', db.String(100), nullable=False)
    email = db.Column('email', db.String(50), nullable=False)
    balance = db.Column('balance', db.Float, nullable=False)
    roles = db.relationship('Role', secondary='user_role',
                            backref=db.backref('users', lazy='dynamic'))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, login, passhash, email, balance, *args):
        super().__init__(*args)
        self.login = login
        self.passhash = passhash
        self.email = email
        self.balance = balance

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.login

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Outcome(db.Model):
    __tablename__ = 'possible_outcome'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False, unique=True)


class Draw(BaseModel, db.Model):
    __tablename__ = 'draw'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)


class Event(BaseModel, db.Model):
    __tablename__ = 'event'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)

    draw_fk = db.Column('draw_fk', db.Integer, db.ForeignKey('draw.id', ondelete='RESTRICT', onupdate='CASCADE'),
                        nullable=False)
    outcome_fk = db.Column('outcome_fk', db.Integer,
                           db.ForeignKey('possible_outcome.id', ondelete='RESTRICT', onupdate='CASCADE'),
                           nullable=False)


class Parlay(BaseModel, db.Model):
    __tablename__ = 'parlay'

    id = db.Column('id', db.Integer, primary_key=True)
    amount = db.Column('amount', db.Float, nullable=False)
    user_fk = db.Column('user_fk', db.String(50), db.ForeignKey('user.login', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)


class ParlayDetails(db.Model):
    __tablename__ = 'parlay_details'

    parlay_fk = db.Column('parlay_fk', db.Integer, db.ForeignKey('parlay.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False, primary_key=True)
    event_fk = db.Column('event_fk', db.Integer, db.ForeignKey('event.id', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, primary_key=True)
    outcome_fk = db.Column('outcome_fk', db.Integer,
                           db.ForeignKey('possible_outcome.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False, primary_key=True)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.String(50), db.ForeignKey('user.login', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)

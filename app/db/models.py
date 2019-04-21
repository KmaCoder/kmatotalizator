from flask_user import UserMixin

from app.db import db

__all__ = ['User', 'Outcome', 'Draw', 'Event', 'Parlay', 'ParlayDetails', 'UserRoles', 'Role']


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    balance = db.Column(db.Float, nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    # active = db.Column(db.Boolean(), nullable=False, server_default='0')
    active = True


class Outcome(db.Model):
    __tablename__ = 'possible_outcomes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Draw(db.Model):
    __tablename__ = 'draws'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    draw_fk = db.Column(db.Integer, db.ForeignKey('draws.id', ondelete='RESTRICT', onupdate='CASCADE'),
                        nullable=False)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='RESTRICT', onupdate='CASCADE'),
                           nullable=False)


class Parlay(db.Model):
    __tablename__ = 'parlays'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_fk = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)


class ParlayDetails(db.Model):
    __tablename__ = 'parlay_details'

    parlay_fk = db.Column(db.Integer, db.ForeignKey('parlays.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False, primary_key=True)
    event_fk = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, primary_key=True)
    outcome_fk = db.Column(db.Integer,
                           db.ForeignKey('possible_outcomes.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False, primary_key=True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)

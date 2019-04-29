from functools import reduce

from flask_user import UserMixin
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

from app.db import db

__all__ = ['User', 'Outcome', 'Draw', 'Event', 'Parlay', 'ParlayDetails', 'UserRoles', 'Role', 'DrawStatus']


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Outcome(db.Model):
    __tablename__ = 'possible_outcomes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class DrawStatus(db.Model):
    __tablename__ = 'draw_statuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # required fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = True

    # custom fields
    username = db.Column(db.String(50), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0)

    # roles relationship
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'),
                        primary_key=True)


class Draw(db.Model):
    __tablename__ = 'draws'

    events_amount = 15
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    datetime_first_match = db.Column(db.DateTime, nullable=True)
    draw_status = db.relationship('DrawStatus')
    events = db.relationship('Event', back_populates="draw")

    draw_status_fk = db.Column(db.Integer, db.ForeignKey('draw_statuses.id', ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=False, default=0)

    @hybrid_property
    def pool_amount(self):
        # return reduce((lambda event_, sum_e: reduce((lambda parlay_, sum_p: parlay_.amount + sum_p), event_) + sum_e), self.events)
        result = 0
        for e in self.events:
            for p in e.parlays:
                result += p.amount
        return result


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    draw = db.relationship('Draw', back_populates="events")
    outcome = db.relationship('Outcome')
    parlays = db.relationship('Parlay', secondary='parlay_details', backref=db.backref('parlays', lazy='dynamic'))

    draw_fk = db.Column(db.Integer, db.ForeignKey('draws.id', ondelete='RESTRICT', onupdate='CASCADE'),
                        nullable=False)
    outcome_fk = db.Column(db.Integer, db.ForeignKey('possible_outcomes.id', ondelete='RESTRICT', onupdate='CASCADE'))


class Parlay(db.Model):
    __tablename__ = 'parlays'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


@event.listens_for(Role.__table__, 'after_create')
def init_roles(*args, **kwargs):
    db.session.add(Role(name="admin"))
    db.session.commit()


@event.listens_for(Outcome.__table__, 'after_create')
def init_outcomes(*args, **kwargs):
    db.session.add(Outcome(name="w1"))
    db.session.add(Outcome(name="X"))
    db.session.add(Outcome(name="w2"))
    db.session.commit()


@event.listens_for(DrawStatus.__table__, 'after_create')
def init_draws(*args, **kwargs):
    db.session.add(DrawStatus(name="hidden"))
    db.session.add(DrawStatus(name="pending"))
    db.session.add(DrawStatus(name="processing"))
    db.session.add(DrawStatus(name="finished"))
    db.session.commit()


@event.listens_for(UserRoles.__table__, 'after_create')
def init_users(*args, **kwargs):
    from app.db.db_repo import database_repo
    database_repo.create_user(username="admin", password="admin", is_admin=True)
    database_repo.create_user(username="KmaCoder", password="4110")
    db.session.commit()


@event.listens_for(ParlayDetails.__table__, 'after_create')
def init_test_data(*args, **kwargs):
    # db.session.add(Role(name="admin"))
    # db.session.commit()
    pass

import datetime
from db.database import db

__all__ = ['User', 'Outcome', 'Draw', 'Event', 'Parlay', 'ParlayDetails']


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
    balance = db.Column('balance', db.Float, nullable=False)

    def __init__(self, login, passhash, balance, *args):
        super().__init__(*args)
        self.login = login
        self.passhash = passhash
        self.balance = balance


class Outcome(BaseModel, db.Model):
    __tablename__ = 'possible_outcome'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)


class Draw(BaseModel, db.Model):
    __tablename__ = 'draw'

    id = db.Column('id', db.Integer, primary_key=True)


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
    amount =db.Column('amount', db.Float, nullable=False)
    user_fk = db.Column('user_fk', db.String(50), db.ForeignKey('user.login', ondelete='CASCADE', onupdate='CASCADE'),
              nullable=False)


class ParlayDetails(BaseModel, db.Model):
    __tablename__ = 'parlay_details'

    parlay_fk = db.Column('parlay_fk', db.Integer, db.ForeignKey('parlay.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False, primary_key=True)
    event_fk = db.Column('event_fk', db.Integer, db.ForeignKey('event.id', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, primary_key=True)
    outcome_fk = db.Column('outcome_fk', db.Integer,
                           db.ForeignKey('possible_outcome.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False, primary_key=True)

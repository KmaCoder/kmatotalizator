import random
from datetime import datetime
from functools import reduce

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

from app.exceptions.controller_exceptions import PlaceBetException
from app.exceptions.db_exceptions import DrawEventsOverflowException, DrawFundsDistributionException
from app.db.models import *


class DatabaseRepo:

    def __init__(self):
        self.db: SQLAlchemy = None
        self.user_manager: UserManager = None

    def init_db(self, db_sqlalchemy: SQLAlchemy, user_manager: UserManager):
        self.db: SQLAlchemy = db_sqlalchemy
        self.user_manager: UserManager = user_manager

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

    def get_draw_by_id(self, draw_id) -> Draw:
        return Draw.query.get(draw_id)

    def get_all_draws(self):
        return Draw.query.order_by(Draw.id.desc()).all()

    def get_all_possible_outcomes(self):
        return Outcome.query.order_by(Outcome.id).all()

    def get_pending_draws(self):
        datetime_now = datetime.now()
        return Draw.query.filter(Draw.datetime_first_match > datetime_now).order_by(Draw.datetime_first_match.desc())

    def create_draw(self, draw_name) -> Draw:
        draw = Draw(name=draw_name)
        self.db.session.add(draw)
        self.db.session.commit()
        return draw

    def add_random_events_to_draw(self, draw: Draw, date):
        while len(draw.events) < draw.events_amount:
            self.create_event("Team1 - Team2", date, draw)
            self.db.session.commit()

    def set_random_draw_outcomes(self, draw: Draw):
        for event in draw.events:
            self.update_event_outcome(event.id,
                                      self.db.session.query(Outcome)[random.randrange(0, Outcome.query.count())])
            self.db.session.commit()

    def create_event(self, event_name, event_datetime, draw: Draw, outcome: Outcome = None) -> Event:
        if len(draw.events) >= draw.events_amount:
            raise DrawEventsOverflowException

        event = Event(name=event_name, datetime=event_datetime, draw=draw, outcome=outcome)
        self.db.session.add(event)

        if draw.datetime_first_match is None or (draw.datetime_first_match - event_datetime).total_seconds() > 0:
            draw.datetime_first_match = event_datetime

        self.db.session.commit()
        return event

    def get_event_by_id(self, event_id) -> Event:
        return Event.query.get(event_id)

    def update_event_outcome(self, event_id, outcome_id):
        self.get_event_by_id(event_id=event_id).outcome_fk = outcome_id
        draw = self.get_event_by_id(event_id).draw
        if self._check_draw_waiting_for_distribution(draw):
            self._distribute_pool(draw)

        self.db.session.commit()

    def place_bet(self, amount: int, events_data, user: User):
        if len(events_data) < Draw.events_amount:
            raise PlaceBetException(message="Select outcome for every event")

        if user.balance < float(amount):
            raise PlaceBetException(message="Not enough funds")

        parlay = Parlay(amount=amount, user=user)
        self.db.session.add(parlay)
        self.db.session.commit()

        for parlay_info in events_data:
            self.db.session.add(
                ParlayDetails(parlay_fk=parlay.id, outcome_fk=parlay_info['value'], event_fk=parlay_info['name']))

        user.balance -= float(amount)

        self.db.session.commit()
        return parlay

    def _check_draw_waiting_for_distribution(self, draw: Draw):
        if draw.draw_status != "waiting_results":
            return False
        for event in draw.events:
            if event.outcome is None:
                return False
        return True

    def _distribute_pool(self, draw):
        if draw.is_finished:
            raise DrawFundsDistributionException("Draw is already finished!!!")

        # object that will contain all parlays which won
        winner_parlays = {
            9: {
                "percent": 32,
                "parlays": []
            },
            10: {
                "percent": 18,
                "parlays": []
            },
            11: {
                "percent": 10,
                "parlays": []
            },
            12: {
                "percent": 10,
                "parlays": []
            },
            13: {
                "percent": 10,
                "parlays": []
            },
            14: {
                "percent": 10,
                "parlays": []
            },
            15: {
                "percent": 10,
                "parlays": []
            }
        }

        # adding parlays to the winner_parlays object
        for parlay in draw.all_parlays:
            # calculating number of correct outcomes for each parlay
            correct_outcomes = reduce(lambda sum_, detail_: int(detail_.outcome.id == detail_.event.outcome.id) + sum_,
                                      parlay.parlay_details, 0)

            # adding parlay to winner_parlays object
            for i in range(min(winner_parlays.keys()), correct_outcomes + 1):
                winner_parlays[i]["parlays"].append(parlay)

        # calculating the prize fund (10% is going to the company)
        draw_prize_fund = draw.pool_amount * 0.9

        # calculating win sum for every parlay and credit gains to users
        for score, group in winner_parlays.items():
            if len(group["parlays"]) == 0:
                continue

            group_money_sum = draw_prize_fund * group["percent"] / 100
            parlays_money_sum = reduce(lambda sum_, parlay_: parlay_.amount + sum_, group["parlays"], 0)
            coeficient = group_money_sum / parlays_money_sum

            for parlay in group["parlays"]:
                parlay_win_sum = parlay.amount * coeficient
                parlay.win_sum = parlay_win_sum if parlay.win_sum is None else parlay.win_sum + parlay_win_sum
                parlay.user.balance += parlay_win_sum

        draw.is_finished = True
        self.db.session.commit()

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

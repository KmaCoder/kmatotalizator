from flask import Flask
from flask_bower import Bower

from app.controllers.user_controller import CustomUserManager
from config import config_object
from app.db.models import User


def create_app():
    # init app obj with config
    app = Flask(__name__)
    app.config.from_object(config_object)

    # init db
    from app.db import db
    db.init_app(app)
    db.app = app

    # include bower components
    Bower(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app=app, db=db, UserClass=User)

    # Setup db repo
    from app.db.db_repo import database_repo
    database_repo.init_db(db, user_manager)

    # create db
    with app.test_request_context():
        db.create_all()

    # register blueprints
    from app.controllers import index_blueprint, admin_blueprint, user_blueprint, game_blueprint
    app.register_blueprint(index_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(game_blueprint)

    return app
#
#
# def create_admins(admins):
#     from app.db.db_repo import database_repo
#     for admin in admins:
#         if database_repo.get_user_by_username(admin['username']) is None:
#             database_repo.create_user(username=admin['username'], password=admin['password'], is_admin=True)

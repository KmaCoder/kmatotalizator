from flask import Flask
from flask_bower import Bower

from app.controllers.user_controller import login_manager, user_manager
from app.db.database import db
from app.db.models import User
from app.controllers import *


def create_app():
    # init app obj with config
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # init database
    db.init_app(app)
    db.app = app
    with app.test_request_context():
        db.create_all()

    # init login manager and user manager
    login_manager.init_app(app)
    user_manager.init_app(app=app, db=db, UserClass=User)

    # include bower components
    Bower(app)

    # register blueprints
    app.register_blueprint(index_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(game_blueprint)

    # add admin user
    create_admin()

    return app


def create_admin():
    """Creates the admin user."""
    from app.db.db_repo import database_repo
    if database_repo.get_user('admin') is None:
        database_repo.create_user(login="admin", password="admin", is_admin=True)

from flask import Flask
from flask_bower import Bower
from flask_login import LoginManager

from app.db.database import db
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

    # init login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    # include bower components
    Bower(app)

    # register blueprints
    app.register_blueprint(index_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(game_blueprint)

    return app

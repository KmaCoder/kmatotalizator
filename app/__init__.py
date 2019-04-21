from flask import Flask
from flask_bower import Bower
from flask_user import UserManager
from config import config_object

from app.db.models import User

def create_app():
    # init app obj with config
    app = Flask(__name__)
    app.config.from_object(config_object)

    # init database
    from app.db import db
    db.init_app(app)
    db.app = app
    with app.test_request_context():
        db.create_all()

    # include bower components
    Bower(app)

    # Setup Flask-User
    user_manager = UserManager(app=app, db=db, UserClass=User)

    # Setup db repo
    from app.db.db_repo import database_repo
    database_repo.init_db(db, user_manager)

    # register blueprints
    from app.controllers import index_blueprint, admin_blueprint, user_blueprint, game_blueprint
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
    if database_repo.get_user_by_username('admin') is None:
        database_repo.create_user(username="admin", password="admin", is_admin=True)

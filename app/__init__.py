from flask import Flask
from flask_bower import Bower
# from sassutils.wsgi import SassMiddleware

from app.controllers.index_controller import index


def create_app():
    # init app obj with config
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # init database
    from app.db.database import db
    db.init_app(app)
    db.app = app
    with app.test_request_context():
        db.create_all()

    # include bower components
    Bower(app, )

    # register blueprints
    app.register_blueprint(index)

    # compile sass
    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'app': ('static/sass', 'static/css', '/static/css', False)
    # })

    return app

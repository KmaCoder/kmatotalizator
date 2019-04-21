import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    PORT = 8000
    HOST = "localhost"
    SECRET_KEY = os.getenv("SECRET_KEY")

    # db properties
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASS = os.getenv('DB_PASS')
    DB_USER = os.getenv('DB_USER')

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    BOWER_COMPONENTS_ROOT = '../bower_components'
    USER_ENABLE_EMAIL = False


class ProductionConfig(Config):
    PORT = 80
    HOST = "0.0.0.0"
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


config_object = DevelopmentConfig()

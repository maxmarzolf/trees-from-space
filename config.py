import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Configuration:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True


class Development(Configuration):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_DATABASE_URL")
    DEBUG = True
    TESTING = True


class Production(Configuration):
    # TODO create production database url
    SQLALCHEMY_DATABASE_URI = load_dotenv("PRODUCTION_DATABASE_URL")
    DEBUG = False
    TESTING = False

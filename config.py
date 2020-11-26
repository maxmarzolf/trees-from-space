from os import environ


class Configuration:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True


class Development(Configuration):
    DEBUG = True
    TESTING = True


class Production(Configuration):
    DEBUG = False
    TESTING = False

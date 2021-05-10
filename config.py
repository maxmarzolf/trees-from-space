import os
from os.path import join, dirname
from dotenv import load_dotenv
import stripe

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Development:
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_DATABASE_URI")
    DEBUG = True
    TESTING = False

    test_stripe_keys = {
        "secret_key": os.environ["TEST_STRIPE_SECRET_KEY"],
        "publishable_key": os.environ["TEST_STRIPE_PUBLISHABLE_KEY"],
        "endpoint_secret": os.environ["TEST_STRIPE_ENDPOINT_SECRET"]
    }


class Production:
    # SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URI")
    DEBUG = False
    TESTING = False

    stripe_keys = {
        "secret_key": os.environ["STRIPE_SECRET_KEY"],
        "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
        "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"]
    }
    stripe.api_key = stripe_keys["secret_key"]

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from website.home.home_routes import home
from website.about.about_routes import about
from website.payment.payment_routes import payment
from website.free.free_routes import free

db = SQLAlchemy()
migrate = Migrate()

from website import models


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        app.register_blueprint(home)
        app.register_blueprint(about)
        app.register_blueprint(payment)
#         app.register_blueprint(free)
        db.create_all()
        return app

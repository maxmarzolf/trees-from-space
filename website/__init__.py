from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

from website import models


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from website.home.home_routes import home_bp
        app.register_blueprint(home_bp)

        from website.product.product_routes import product_bp
        app.register_blueprint(product_bp)

        from website.checkout.checkout_routes import checkout_bp
        app.register_blueprint(checkout_bp)

        from website.payment.payment_routes import payment_bp
        app.register_blueprint(payment_bp)

        # only called if the tables have not been created
        # db.create_all()

        return app

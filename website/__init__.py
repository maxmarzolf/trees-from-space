from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from website.home.home_routes import home_bp
        app.register_blueprint(home_bp)

        from website.product.product_routes import product_bp
        app.register_blueprint(product_bp)

        from website.checkout.checkout_routes import checkout_bp
        app.register_blueprint(checkout_bp)

        from website.payment.payment_routes import payment_bp
        app.register_blueprint(payment_bp)

        return app

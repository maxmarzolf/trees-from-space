from flask import Blueprint

payment = Blueprint("payment_bp", __name__, static_folder="website.static",
                    template_folder="website.templates")
test_payment = Blueprint("test_payment_bp", __name__, static_folder="website.static",
                        template_folder="website.templates")

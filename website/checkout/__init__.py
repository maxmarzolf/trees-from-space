from flask import Blueprint

checkout_bp = Blueprint("checkout_bp", __name__, static_folder="website.static",
                        template_folder="website.templates")

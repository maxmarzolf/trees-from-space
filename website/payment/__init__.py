from flask import Blueprint

payment_bp = Blueprint("payment_bp", __name__, static_folder="website.static", template_folder="website.templates")

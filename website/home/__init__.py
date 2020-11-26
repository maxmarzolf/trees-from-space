from flask import Blueprint

home_bp = Blueprint('home_bp', __name__, static_folder="website.static",
                    template_folder="website.templates")


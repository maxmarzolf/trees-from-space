from flask import Blueprint

about_bp = Blueprint('about_bp', __name__, static_folder="website.static",
                     template_folder="website.templates")

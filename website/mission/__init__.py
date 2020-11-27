from flask import Blueprint

mission_bp = Blueprint('mission_bp', __name__, static_folder="website.static",
                       template_folder="website.templates")

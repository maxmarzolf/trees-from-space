from flask import Blueprint

home = Blueprint('home', __name__, static_folder="website.static",
                 template_folder="website.templates")

from flask import Blueprint

free = Blueprint('free', __name__, static_folder="website.static",
                  template_folder="website.templates")

from flask import Blueprint

about = Blueprint('about', __name__, static_folder="website.static",
                  template_folder="website.templates")

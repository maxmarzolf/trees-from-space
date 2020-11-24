from flask import Blueprint

product_bp = Blueprint('product_bp', __name__, static_folder="website.static",
                       template_folder="website.templates")

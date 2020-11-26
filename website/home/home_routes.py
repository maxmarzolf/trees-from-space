from flask import render_template
from website.home import home_bp


@home_bp.route("/")
def land_here():
    return render_template("home/home.html")

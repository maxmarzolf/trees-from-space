from flask import render_template
from website.home import home


@home.route("/")
def initialize():
    return render_template("home/home.html")

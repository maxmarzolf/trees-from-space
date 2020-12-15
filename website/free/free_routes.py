from flask import render_template
from website.free import free


@free.route('/free')
def initialize():
    return render_template('free/free.html')

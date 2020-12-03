from flask import render_template
from website.mission import about_bp


@about_bp.route('/about')
def land_here():
    return render_template('about/about.html')

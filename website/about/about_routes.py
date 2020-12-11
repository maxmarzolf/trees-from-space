from flask import render_template
from website.about import about


@about.route('/about')
def land_here():
    return render_template('about/about.html')

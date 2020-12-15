from flask import render_template
from website.about import about


@about.route('/about')
def initialize():
    return render_template('about/about.html')

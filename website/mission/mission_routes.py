from flask import render_template
from website.mission import mission_bp


@mission_bp.route('/mission')
def land_here():
    return render_template('mission/mission.html')

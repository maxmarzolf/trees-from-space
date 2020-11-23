from flask import render_template
from website.payment import payment_bp


@payment_bp.route('/payment')
def land_here():
    return render_template("payment/payment.html")

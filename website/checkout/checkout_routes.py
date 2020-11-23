from flask import render_template
from website.checkout import checkout_bp


@checkout_bp.route("/checkout")
def land_here():
    return render_template("checkout/checkout.html")

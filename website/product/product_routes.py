from flask import render_template
from website.product import product_bp


@product_bp.route('/product')
def land_here():
    return render_template('product/product.html')

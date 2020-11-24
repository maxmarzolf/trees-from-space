from app import db


class Order(db.Model):
    id = db.Column(db.Integer(), nullable=False)
    datetime = db.Column(db.datetime(), nullable=False)
    name = db.Column(db.string(150), nullable=False)
    email = db.Column(db.string(150), nullable=False)
    order = db.Column(db.string(150), nullable=False)
    total = db.Column(db.Numeric, nullable=False)

from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'ORDER'
    id = db.Column(db.Integer(), primary_key=True)
    datetime = db.Column(db.datetime(), nullable=False, default=datetime.now())
    name = db.Column(db.string(150), nullable=False)
    email = db.Column(db.string(150), nullable=False)
    order = db.Column(db.string(150), nullable=False)
    total = db.Column(db.Numeric(precision(8, 4)), nullable=False)

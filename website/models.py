from website import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'ORDER'
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    total = db.Column(db.Numeric(8, 4), nullable=False)


class Product(db.Model):
    __tablename__ = 'PRODUCT'
    name = db.Column(db.String(150), primary_key=True)
    description = db.Column(db.String(150), nullable=False)
    inventory = db.Column(db.Enum(
        decals=0,
        small=0,
        medium=0,
        large=0
    ), nullable=False)
    sizes = db.Column(db.String(25), nullable=True)
    price = db.Column(db.Numeric(2, 2), nullable=False)
    image = db.Column(db.BLOB, nullable=True)

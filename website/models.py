from website import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'ORDER'
    id = db.Column(db.Integer(), primary_key=True)
    datetime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    order = db.Column(db.String(150), nullable=False)
    total = db.Column(db.Numeric(8, 4), nullable=False)


class ShirtInventory(db.Model):
    __tablename__ = 'SHIRT_INVENTORY'
    id = db.Column(db.Integer(), primary_key=True)
    small = db.Column(db.Integer())
    medium = db.Column(db.Integer())
    large = db.Column(db.Integer())


class DecalInventory(db.Model):
    __tablename__ = 'DECAL_INVENTORY'
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer())

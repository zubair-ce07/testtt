import json

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import Session , relationship

from flask_login import UserMixin
from . import db

engine = create_engine('mysql://root:passroot@localhost/crudapplication')
db.metadata.bind = engine
session = Session(engine)

class User(UserMixin, db.Model):
    __tablename__ = 'accounts'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    password = db.Column('password', db.String)
    address = db.Column('address', db.String)
    children = relationship("Order")

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('accounts.id'))
    status = db.Column(String, default="Pending")
    children = relationship("Cart")

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    price = db.Column('price', db.Integer)
    unit = db.Column('unit', db.String)
    inventory = db.Column('inventory', db.Integer)
    image_path = db.Column('image_path', db.String)
    children = relationship("Cart")

    def row2json(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(Integer, primary_key=True)
    item_id = db.Column(Integer, ForeignKey('items.id'))
    quantity = db.Column(Integer)
    order_id = db.Column(Integer, ForeignKey('orders.id'))     
   
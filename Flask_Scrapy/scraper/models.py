import sqlalchemy as alc

from .database import Base


class Item(Base):
    __tablename__ = 'items'
    id = alc.Column(alc.Integer, primary_key=True, autoincrement=True)
    identifier = alc.Column(alc.Integer)
    retailer_sku = alc.Column(alc.Integer)
    color_name = alc.Column(alc.VARCHAR(50))
    skus = alc.Column(alc.PickleType)
    availability = alc.Column(alc.BOOLEAN)
    image_urls = alc.Column(alc.PickleType)
    description = alc.Column(alc.PickleType)
    currency = alc.Column(alc.VARCHAR(10))
    category = alc.Column(alc.PickleType)
    url = alc.Column(alc.VARCHAR(200))
    product_name = alc.Column(alc.VARCHAR(100))
    brand = alc.Column(alc.VARCHAR(50))
    referrer_url = alc.Column(alc.VARCHAR(200))

    def __init__(self, item):
        self.skus = [sku._values for sku in item['skus']]
        self.availability = item['availability']
        self.image_urls = item['image_urls']
        self.description = item['description']
        self.currency = item['currency']
        self.category = item['category']
        self.url = item['url']
        self.product_name = item['product_name']
        self.brand = item['brand']
        self.retailer_sku = item['retailer_sku']
        self.identifier = item['identifier']
        self.color_name = item['color_name']
        self.referrer_url = item['referrer_url']


class User(Base):
    __tablename__ = 'users'
    id = alc.Column(alc.Integer, primary_key=True, autoincrement=True)
    username = alc.Column(alc.Text, unique=True, nullable=False)
    password = alc.Column(alc.Text, nullable=False)

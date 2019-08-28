from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine('sqlite:///products.sqlite')


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Product(DeclarativeBase):
    __tablename__ = "Product"

    retailer_sku = Column(String, primary_key=True)
    gender = Column(String)
    category = Column(String)
    brand = Column(String)
    url = Column(String)
    date = Column(String)
    currency = Column(String)
    market = Column(String)
    retailer = Column(String)
    url_original = Column(String)
    name = Column(String)
    description = Column(String)
    care = Column(String)
    price = Column(Integer)
    spider_name = Column(String)
    crawl_start_time = Column(String)


class ImageURLS(DeclarativeBase):
    __tablename__ = "ImageURLS"

    retailer_sku = Column(String, ForeignKey('Product.retailer_sku'), primary_key=True)
    image_urls = Column(String)


class SKUS(DeclarativeBase):
    __tablename__ = "SKUS"

    sku_id = Column(String, primary_key=True)
    retailer_sku = Column(String, ForeignKey('Product.retailer_sku'))
    currency = Column(String)
    price = Column(Integer)
    size = Column(String)
    out_of_stock = Column(Boolean)

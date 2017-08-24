from sqlalchemy import create_engine, Column, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship

import settings

Base = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    Base.metadata.create_all(engine)


class Product(Base):
    __tablename__ = "product"
    store_keeping_unit = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    product_url = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    description = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    variation = relationship("Product_Variation", uselist=False, back_populates="product")
    size = relationship("Product_Size", uselist=False, back_populates="product")


class Product_Variation(Base):
    __tablename__ = "variation"
    store_keeping_unit = Column(String, ForeignKey("product.store_keeping_unit"), primary_key=True)
    display_color_name = Column(String, primary_key=True)
    image_urls = Column(String)
    product = relationship("Product", back_populates="variation")


class Product_Size(Base):
    __tablename__ = "size"
    store_keeping_unit = Column(String, ForeignKey("product.store_keeping_unit"), primary_key=True)
    size_name = Column(String, primary_key=True)
    is_available = Column(Boolean)
    price = Column(String)
    is_discounted = Column(Boolean)
    discounted_price = Column(String)
    product = relationship("Product", back_populates="size")

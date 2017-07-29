from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from books_spider import settings

DeclarativeBase = declarative_base()


def db_connect():

    return create_engine(URL(**settings.DATABASE))


def create_books_table(engine):

    DeclarativeBase.metadata.create_all(engine)


class BooksTable(DeclarativeBase):
    """Sqlalchemy books table model"""
    __tablename__ = "booksRecord"
    id = Column(Integer, primary_key=True)
    Book_Name = Column('Book_Name', String(150))
    Book_price = Column('Book_Price', String(10))
    Book_Author = Column('Book_Author', String(150))
    Image__Img_Url = Column('Image__Img_Url', String(150))
    Book_Category = Column('Book_Category', String(50))
    Book_Condition = Column('Book_Condition', String(20))
    Book_Weight = Column('Book_Weight', String(10))
    Book_Language = Column('Book_Language', String(20))



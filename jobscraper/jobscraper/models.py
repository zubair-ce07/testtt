from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


Base = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_jobs_table(engine):
    Base.metadata.create_all(engine)


class Jobs(Base):
    __tablename__ = 'Jobs'
    job_id = Column(Integer, primary_key=True)
    crawl_id = Column(String)
    crawled_at = Column(DateTime)
    title = Column(String)
    job_nature = Column(String)
    attribute = Column(String)
    job_count = Column(Integer)

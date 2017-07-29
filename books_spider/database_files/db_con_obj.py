# import psycopg2
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
#
#
# engine = create_engine('postgresql+psycopg2://postgres:2321@localhost/postgres')
#
# db = scoped_session(sessionmaker(autocommit=False,
#                                  autoflush=False,
#                                  bind=engine))
# Base = declarative_base()
# # Session = sessionmaker(db)
# # session = Session()
# # Base.metadata.create_all(db)

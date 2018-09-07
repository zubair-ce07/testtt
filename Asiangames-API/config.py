import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'asiangames.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'TACHANKA'
    JWT_SECRET_KEY = 'THATCHER'
    MASTER_PASSWORD = 'ADMIN123'

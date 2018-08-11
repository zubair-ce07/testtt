import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This class contains config variables for our project"""

    #This variable is for protection from CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #These variables are used by flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

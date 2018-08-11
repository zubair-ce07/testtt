from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

"""this import is written at the end to avoid cyclic calls as routes module
    also imports the "app"
"""
from myapp import routes,models #myapp is name of the application , not the object above
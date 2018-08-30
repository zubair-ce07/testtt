from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
marshmallow_app = Marshmallow(app)
api = Api(app)


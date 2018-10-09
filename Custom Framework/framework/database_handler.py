from exceptions import AttributeNotFound, ImproperlyConfigured
from importlib import import_module

from peewee import Model, Proxy, SqliteDatabase
from utils import get_settings

settings = get_settings()

database_proxy = Proxy()


def intialize_database():
    with DatabaseConnection() as db:
        db_models_module = get_models_module()
        models = get_models(db_models_module)
        for model in models:
            module = getattr(db_models_module, model)
            db.create_tables([module])


def get_models_module():
    try:
        db_models = import_module(settings.DB_MODELS)
    except ImportError:
        raise ImproperlyConfigured("{0} is not available in your application folder".format(settings.DB_MODELS))
    return db_models


def get_models(db_models_module):
    try:
        models = db_models_module.models
    except AttributeError:
        raise AttributeNotFound(
            "Please set your variable `models(list)` which contains all your models name in {0}".format(
                db_models_module
            ))
    return models


class DatabaseConnection(object):
    def __init__(self):
        try:
            self.db = SqliteDatabase(settings.DB_URL)
            database_proxy.initialize(self.db)
        except AttributeError as ae:
            raise AttributeNotFound(
                "Please set DB_URL variable in your settings.py file"
            )

    def __enter__(self):
        self.db.connect()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


class BaseModel(Model):
    class Meta:
        database = database_proxy

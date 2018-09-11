import os
from exceptions import ImproperlyConfigured
from importlib import import_module


def get_settings():
    try:
        settings = import_module(os.getenv("application_settings"))
    except ImportError:
        raise ImproperlyConfigured("Please set your Application Settings file path in load.py")

    return settings

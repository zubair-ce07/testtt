import os
from os.path import abspath, dirname, join


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'insecure_secret_key'
TMDB_API_KEY = 'obtain_your_api_key_from_tmdb'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_celery_beat',
    'django_celery_results',
    'movies',
    'users',
    'watchlists',
]

WSGI_APPLICATION = 'movie_time.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'movie_time.urls'

CELERY_RESULT_BACKEND = 'django-db'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if os.path.isfile(join(dirname(abspath(__file__)), 'conf.py')):
    from movie_time.conf import *

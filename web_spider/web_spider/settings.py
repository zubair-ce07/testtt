import os
from os.path import abspath, dirname, join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# if config not found will use this default
SECRET_KEY = 'sample_secret_key'

DEBUG = True

ALLOWED_HOSTS = []

# Some apps required for logging in admin
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'url_crawler',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'web_spider.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_spider.wsgi.application'

# if config not found will use this default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = 'login'
AUTH_USER_MODEL = 'url_crawler.CustomUser'

AUTHENTICATION_BACKENDS = (
    'url_crawler.auth_backend.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

STATIC_URL = '/static/'

if os.path.isfile(join(dirname(abspath(__file__)), 'conf.py')):
    from web_spider.conf import *

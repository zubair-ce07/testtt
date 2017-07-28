import os
from os.path import abspath, dirname, join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# if config not found will use this default
SECRET_KEY = 'sample_secret_key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'user_api',
    'rest_framework',
    'rest_framework.authtoken'
]

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    # using Token authentication for user api
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'motion_pictures.urls'

AUTH_USER_MODEL = 'user_api.User'
# using custom authentication backend
AUTHENTICATION_BACKENDS = (
    'user_api.auth_backend.CustomAuthBackend',
)

WSGI_APPLICATION = 'motion_pictures.wsgi.application'

# if config not found will use this default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

if os.path.isfile(join(dirname(abspath(__file__)), 'conf.py')):
    from motion_pictures.conf import *

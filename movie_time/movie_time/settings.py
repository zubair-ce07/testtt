import os
from os.path import abspath, dirname, join


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'insecure_secret_key'
TMDB_API_KEY = 'obtain_your_api_key_from_tmdb'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'corsheaders',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'rest_framework.authtoken',
    'movies',
    'users',
    'watchlists',
]

WSGI_APPLICATION = 'movie_time.wsgi.application'

REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
INTERNAL_IPS = ('127.0.0.1', )

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'users.auth_backend.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ROOT_URLCONF = 'movie_time.urls'

CELERY_RESULT_BACKEND = 'django-db'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(dirname(dirname(abspath(__file__))), 'media')

if os.path.isfile(join(dirname(abspath(__file__)), 'conf.py')):
    from movie_time.conf import *

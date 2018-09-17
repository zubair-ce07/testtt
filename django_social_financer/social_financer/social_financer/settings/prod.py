__author__ = 'abdul'

from social_financer.settings.base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', 'localhost']

WSGI_APPLICATION = 'social_financer.wsgi.prod_application'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

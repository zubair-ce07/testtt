"""
WSGI config for social_financer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from .settings import prod

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_financer.settings.dev')

application = get_wsgi_application()
prod_application = WhiteNoise(application, root=prod.STATIC_ROOT)

"""
WSGI config for DjangoRestReactSocialApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from social_app.views import sio
import socketio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRestReactSocialApp.settings')

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)

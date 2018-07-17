from __future__ import absolute_import, unicode_literals

import os
import djcelery

from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forms.settings')
app = Celery('forms')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_get_thenews_article_every_minutes',
          Exchange('for_get_thenews_article_every_minutes'),
          routing_key='for_get_thenews_article_every_minutes'),
)
CELERY_ROUTES = {
    'my_get_thenews_article_every_minutes': {
        'queue': 'for_get_thenews_article_every_minutes',
        'routing_key': 'for_get_thenews_article_every_minutes'},
}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULE = {
    # Executes after every 10 minutes.
    'get_thenews_article_every_minutes': {
        'task': 'get_thenews_article_every_minutes',
        'schedule': timedelta(minutes=10),
    }
}
djcelery.setup_loader()

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_time.settings')

app = Celery('movie_time')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.control.rate_limit('movies.tasks.get_new_movie', '230/m')

# app.conf.beat_schedule = {
#     'get_movie_every_minute': {
#         'task': 'movies.tasks.retrieve_movies',
#         'schedule': crontab(minute='*/15')
#     },
# }

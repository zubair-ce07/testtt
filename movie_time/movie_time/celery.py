from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_time.settings')

app = Celery('movie_time')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_changes_every_day': {
        'task': 'movies.tasks.updates_in_movies',
        'schedule': crontab(minute=0, hour=6)
    },
    'notify_users_every_day': {
        'task': 'watchlist.tasks.notify_about_newly_released',
        'schedule': crontab(minute=0, hour=6)
    }
}

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from movies.utils import create_movie


@shared_task
def retrieve_movies():
    for tmdb_id in range(1, 10):
        get_new_movie.delay(tmdb_id)
    return 'Task Scheduled'


@shared_task(bind=True, retry_backoff=True, default_retry_delay=10, max_retries=None)
def get_new_movie(self, tmdb_id):
    try:
        return create_movie(tmdb_id)
    except Exception as e:
        raise self.retry(exc=e)

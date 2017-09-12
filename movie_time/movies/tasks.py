from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from movies.utils import create_or_update_movie
from movies.utils import get_changed_movies_ids


@shared_task(bind=True, default_retry_delay=10, max_retries=None)
def updates_in_movies(self):
    current_date = timezone.now().date()
    start_date = str(current_date - timedelta(days=1))
    end_date = str(current_date)
    logger = get_task_logger(__name__)

    try:
        changed_movies = get_changed_movies_ids(start_date, end_date)
    except Exception as e:
        logger.info('Getting change list failed.')
        raise self.retry(exc=e)

    for movie in changed_movies:
        get_new_movie.delay(movie.get('id'))


@shared_task(bind=True, retry_backoff=True, default_retry_delay=10, max_retries=None, rate_limit='220/m')
def get_new_movie(self, tmdb_id):
    logger = get_task_logger(__name__)
    try:
        return create_or_update_movie(tmdb_id)
    except Exception as e:
        logger.info('ID: {} - Failed'.format(tmdb_id))
        raise self.retry(exc=e)

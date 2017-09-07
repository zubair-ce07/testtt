from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from celery.utils.log import get_task_logger
from movies.models import Movie
from users.models import Notification


@shared_task(bind=True, default_retry_delay=10, max_retries=None)
def notify_about_newly_released(self):
    current_date = timezone.now().date()
    logger = get_task_logger(__name__)

    try:
        movies = Movie.objects.filter(
            release_date__year=current_date.year,
            release_date__month=current_date.month,
            release_date__day=current_date.day
        ).prefetch_related('watchlist')
        for movie in movies:
            for item in movie.watchlist:
                Notification.objects.create(
                    recipient=item.user,
                    verb=Notification.MOVIE_RELEASED,
                    action_object=movie
                )
    except Exception as e:
        logger.info('Notify process failed.')
        raise self.retry(exc=e)

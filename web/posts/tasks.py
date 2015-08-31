from __future__ import absolute_import

from celery import shared_task
from django.utils import timezone
from web.posts.models import Post


@shared_task
def validate_posts():
    for post in Post.objects.exclude(is_expired=True):
        time_delta = post.expired_on - timezone.now()
        if time_delta.total_seconds() < 0:
            post.is_expired = True
            post.save()
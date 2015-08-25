import threading
from django.utils import timezone
import time
from web.posts.models import Post


class ValidateAllPostsThread(threading.Thread):

    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.delay = delay

    def run(self):
        while True:
            self.validate_posts()
            time.sleep(self.delay)

    # noinspection PyMethodMayBeStatic
    def validate_posts(self):

        for post in Post.objects.exclude(is_expired=True):
            time_delta = post.expired_on - timezone.now()
            if time_delta.total_seconds() < 0:
                post.is_expired = True
                post.save()

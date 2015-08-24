import threading
from django.utils import timezone
import time
from web.posts.models import Post


class ValidateAllPostsThread(threading.Thread):

    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.delay = delay

    def run(self):
        self.validate_posts(self.delay)

    # noinspection PyMethodMayBeStatic
    def validate_posts(self, delay):
        while True:
            posts = Post.objects.exclude(is_expired=True)
            for post in posts:
                time_delta = post.expired_on - timezone.now()
                if time_delta.total_seconds() < 0:
                    post.is_expired = True
                    post.save()
            time.sleep(delay)
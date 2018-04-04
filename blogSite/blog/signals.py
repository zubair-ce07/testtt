from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from blog.models import Post
from pprint import pprint


@receiver(pre_save, sender=Post)
def pre_save_handler(sender, **kwargs):
    with open('signal_output.txt', 'a') as out:
        pprint('pre save event', stream=out)

@receiver(post_save, sender=Post)
def post_save_handler(sender, **kwargs):
    with open('signal_output.txt', 'a') as out:
        pprint('post save event', stream=out)
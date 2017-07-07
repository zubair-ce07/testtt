from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from .models import Trainee, Trainer, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    This signal is received when a user is created
    and for that a user profile is made
    """
    if created:
        UserProfile.objects.create(user=instance)


add_trainee_signal = Signal(providing_args=['user'])
add_trainer_signal = Signal(providing_args=['user'])


def add_trainee(sender, **kwargs):
    """
    add_trainee Signal is sent when user_profile
    is made during trainee signup
    """
    trainee = Trainee.objects.create(user=kwargs['user'])
    trainer = Trainer.objects.available_trainer()

    if trainer:
        trainee.trainer = trainer

    trainee.save()


def add_trainer(sender, **kwargs):
    """
    add_trainer Signal is sent when user_profile
    is made during trainer signup
    """
    Trainer.objects.create(user=kwargs['user'])


"""
connecting trainer and trainee signals to
trainer and trainee add methods
"""
add_trainee_signal.connect(add_trainee)
add_trainer_signal.connect(add_trainer)

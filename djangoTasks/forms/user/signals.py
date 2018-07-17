"""This module contains custom signal's functions"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(pre_save, sender=get_user_model())
def lower_name(sender, instance, *args, **kwargs):
    """
    pre-signal reciever for user's model to title their first and last name
    field values and to lower their username's value
    :param sender: particular sender to receieve signal from
    :param instance: instance of user's model
    :param args: arguments
    :param kwargs: keyword arguments dict
    """
    instance.first_name = instance.first_name.title()
    instance.last_name = instance.last_name.title()
    instance.username = instance.username.lower()

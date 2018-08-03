from django import template

from taskmanager import models

register = template.Library()


@register.simple_tag
def total_tasks():
    return models.Task.objects.count()
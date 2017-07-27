from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from todo.models import TodoItem


@receiver(pre_save, sender=TodoItem)
def log_todoitem(sender, instance, **kwargs):
    """
    Logs the id, user of each TodoItem and the current time 
    before each save of TodoItem model
    """
    instance.log += 'Task: %s | User: %s | Time: %s\n' % (
        instance.id, instance.user, timezone.now()
    )

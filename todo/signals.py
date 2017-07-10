from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


from todo.models import TodoItem


@receiver(pre_save, sender=TodoItem)
def log_todoitem(sender, **kwargs):
    '''
    Logs the id, user and time of each TodoItem after each save
    '''
    kwargs['instance'].log += 'Task: %s | User: %s | Time: %s\n' % (
        kwargs['instance'].id, kwargs['instance'].user, timezone.now()
    )
    

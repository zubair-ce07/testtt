from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from datetime import datetime
from memoapp.signals import user_login, user_logout
from memoapp.models import User, Memory, Activity


@receiver(post_save,  sender=Memory)
def after_mem_saved_create_log(sender, instance, created, **kwargs):
    activity = ''
    if created:
        activity = 'Add'
    else:
        activity = 'Edit'
    activity = Activity(memory_title=instance.title, activity=activity, user_id=instance.user_id)
    activity.save()


@receiver(post_delete, sender=Memory)
def after_mem_delete_create_log(sender, instance, **kwargs):
    activity = Activity(memory_title=instance.title,activity='Delete', user_id=instance.user_id)
    activity.save()

@receiver(user_login)
def some_one_logged_in(sender,**kwargs):
    f = open('login_logout.txt', 'a+')
    f.write(kwargs['user_name'] + ' is logged in at ' + str(datetime.now())+ '\n')
    f.close()


@receiver(user_logout)
def some_one_logged_out(sender,**kwargs):
    f = open('login_logout.txt', 'a+')
    f.write(kwargs['user_name'] + ' is logged OUT at ' + str(datetime.now()) + '\n')
    f.close()


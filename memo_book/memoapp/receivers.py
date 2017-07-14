from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import datetime
from memoapp.signals import user_login, user_logout
from memoapp.models import Memory


@receiver(pre_save,  sender=Memory)
def before_user_save(sender, **kwargs):
    print(sender)


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


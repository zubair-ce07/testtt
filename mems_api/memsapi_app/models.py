from django.db import models
from datetime import datetime
from django.contrib.auth.models import  AbstractBaseUser, UserManager
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class PrivateMemoryManager(models.Manager):
    def get_queryset(self):
        return super(PrivateMemoryManager, self).get_queryset().filter(is_public=False)


class PublicMemoryManager(models.Manager):
    def get_queryset(self):
        return super(PublicMemoryManager, self).get_queryset().filter(is_public=True)


class User(AbstractBaseUser):
    image = models.ImageField(upload_to='images/', null=True)
    email = models.EmailField(unique=True)
    first_name =  models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    has_perm = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


    def has_perm(self, arg):
        if self.is_superuser:
            return True
        return False

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

    USERNAME_FIELD = 'email'
    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Memory(models.Model):
    user = models.ForeignKey(User,related_name='mems', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='mems', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    url = models.CharField(max_length=300)
    tags = models.CharField(max_length=200)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', null=True)
    objects = models.Manager()
    private_memories = PrivateMemoryManager()
    public_memories = PublicMemoryManager()

    def __str__(self):
        return self.title


class Activity(models.Model):
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    memory_title = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now())
    activity = models.CharField(choices=(('Add', 'Add'), ('Edit', 'Edit'), ('Delete', 'Delete')),
                                max_length=6)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
from django.contrib.auth.models import User
from django.db import models
<<<<<<< HEAD
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, error_messages={'error': 'Invalid Gender'}, blank=True)
    image = models.ImageField(upload_to='./user-images/', default='user.png', blank=True)
    created_at = models.DateTimeField()


@receiver(post_save, sender=User)
def save_userinfo(sender, instance, created, **kwargs):
    if created:
        user_info = getattr(instance, 'info', None)
        info = UserInfo(user=instance, phone_no=user_info['phone_num'],
                        address=user_info['address'], date_of_birth=user_info['dob'],
                        gender=user_info['gender'], created_at=user_info['created_at']
                        )
        info.save()


=======


class UserInfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1)
    image = models.ImageField(upload_to='./user-images/')
    created_at = models.DateTimeField()


>>>>>>> d6e8908... Adding Main Models
class Blog(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    slug = models.SlugField()
    text = models.TextField()
    summary = models.TextField()
    created_on = models.DateField()
<<<<<<< HEAD
    is_published = models.BooleanField(default=False)
=======
    is_published = models.BooleanField(default=True)
>>>>>>> d6e8908... Adding Main Models
    comments_allowed = models.BooleanField(default=True)
    is_public = models.BooleanField()


class Comment(models.Model):
    text = models.TextField()
    comment_for = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()


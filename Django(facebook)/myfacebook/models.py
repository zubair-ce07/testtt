from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserProfileManager(models.Manager):
    def create_user(self, **cleaned_data):
        user = User(username=cleaned_data['username'],
                    first_name=cleaned_data['first_name'],
                    last_name=cleaned_data['last_name'])
        user.set_password(cleaned_data['password1'])

        post_save.disconnect(create_user_profile, sender=User)
        user.save()
        post_save.connect(create_user_profile, sender=User)

        user_profile = UserProfile(user=user,
                                   gender=cleaned_data['gender'],
                                   date_of_birth=cleaned_data['date_of_birth'])
        user_profile.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    date_of_birth = models.DateField('date of birth', null=True)
    gender_choices = (
        ('Male', u"Male"),
        ('Female', u"Female"),)
    gender = models.CharField(max_length=20, choices=gender_choices)
    objects = UserProfileManager()


class UserStatus(models.Model):
    status_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_status')
    status_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.status_text


class UserFollowers(models.Model):
    followee = models.ForeignKey(User, related_name="followee")
    follower = models.ForeignKey(User, related_name="followers")

    class Meta:
        unique_together = ('followee', 'follower')


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    date = models.DateField('date published')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    detail = models.TextField(max_length=3000)
    link = models.URLField(max_length=200)
    image_url = models.URLField(max_length=200)

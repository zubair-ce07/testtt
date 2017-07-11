import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from address.models import AddressField
from django.db.models import ImageField


class CustomUser(User):
    class Meta:
        proxy = True
        ordering = ('first_name', )

    def save(self, *args, **kwargs):
        print(kwargs)
        # kwargs_temp = kwargs
        # kwargs = {}
        # kwargs = kwargs_temp

        self._up = kwargs['up']
        print(type(kwargs['up']))
        # print(kwargs['phone_number'])
        kwargs = {}
        super(CustomUser, self).save(*args, **kwargs)
        # kwargs = {'phone_number': '1234567891'}
        print(kwargs)


# def get_image_path(instance, filename):
#     return os.path.join('photos', str(instance.id), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    test = models.CharField(max_length=10)
    phone_number = models.CharField(validators=[RegexValidator(
        regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")], max_length=15)
    country = CountryField(blank=True, null=True)
    image = ImageField(upload_to='users/', blank=True, null=True)
    address = AddressField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    test = models.CharField(max_length=10)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    print('*******************************************************************')
    # phone_number = getattr(instance, '_phone_number')
    up = kwargs['_up']
    # print(phone_number)
    if created:
        up.save()


# @receiver(post_save, sender=User)
# # def create_or_update_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         UserProfile.objects.create(user=instance)
# #     instance.userprofile.save()
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

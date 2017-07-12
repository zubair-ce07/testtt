import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django_countries.fields import CountryField, Country
from address.models import AddressField, Address
from django.db.models import ImageField
from django_countries.data import COUNTRIES

COUNTRIES_NAMES = dict([[v, k] for k, v in COUNTRIES.items()])


class CustomUser(User):
    class Meta:
        proxy = True
        ordering = ('first_name', )

    def save(self, *args, **kwargs):
        # kwargs_temp = kwargs
        # print(kwargs['phone_number'])
        self._phone_number = kwargs['phone_number']
        self._country_name = kwargs['country_name']
        self._address = kwargs['address']
        self._image = kwargs['image']
        print(self._image)
        kwargs = {}
        # CustomUser.set_password(self.passwordestpassword1')
        super(CustomUser, self).save(*args, **kwargs)
        # kwargs = kwargs_temp
        # print(kwargs_temp)
        # print(kwargs)

        # print(kwargs['phone_number'])

        # kwargs = {'phone_number': '1234567891'}
        # print(kwargs)


# def get_image_path(instance, filename):
#     return os.path.join('photos', str(instance.id), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # test = models.CharField(max_length=10)
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
    phone_number = getattr(instance, '_phone_number')
    country_name = getattr(instance, '_country_name')
    address_raw = getattr(instance, '_address')
    image = getattr(instance, '_image')
    print(image)
    # print(address1)
    # print(address_raw)
    # phone_number = kwargs['_phone_number']
    # print(phone_number)
    if created:
        # image = ImageField(name=image)
        print(image)
        address1 = Address(raw=address_raw)
        country = Country(code=COUNTRIES_NAMES[country_name])
        address1.save()
        u = UserProfile(user=instance, phone_number=phone_number,
                        country=country, address=address1)
        print(type(u.image))
        u.image.name = image
        print(u.image.name)
        u.save()


# @receiver(post_save, sender=User)
# # def create_or_update_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         UserProfile.objects.create(user=instance)
# #     instance.userprofile.save()
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

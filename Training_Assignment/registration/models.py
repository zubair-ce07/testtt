import os
from shutil import copy2

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django_countries.fields import CountryField, Country
from address.models import AddressField, Address
from django.db.models.fields.files import FileField, ImageFieldFile, ImageField
from django_countries.data import COUNTRIES

from task1.settings import MEDIA_ROOT

COUNTRIES_NAMES = dict([[v, k] for k, v in COUNTRIES.items()])


class CustomUser(User):
    class Meta:
        proxy = True
        ordering = ('first_name', )

    def save(self, *args, **kwargs):
        try:
            self._phone_number = kwargs['phone_number']
            self._country_name = kwargs['country_name']
            self._address = kwargs['address']
            self._image = kwargs['image']
        except:
            print('bla')
        kwargs = {}
        self.full_clean()
        super(CustomUser, self).save(*args, **kwargs)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[RegexValidator(
        regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")], max_length=15)
    country = CountryField(blank=True, null=True)
    image = ImageField(upload_to='registration/', blank=True, null=True)
    address = AddressField(blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        phone_number = getattr(instance, '_phone_number')
        country_name = getattr(instance, '_country_name')
        address_raw = getattr(instance, '_address')
        src = getattr(instance, '_image')
        dest = MEDIA_ROOT + 'registration/' + os.path.basename(src)
        head, tail = os.path.splitext(os.path.basename(src))
        count = 0
        while os.path.exists(dest):
            count += 1
            dest = os.path.join(os.path.dirname(
                dest), '{}-{}{}'.format(head, count, tail))
        copy2(src, dest)
        address = Address(raw=address_raw, formatted=address_raw)
        address.save()
        country = Country(code=COUNTRIES_NAMES[country_name])
        dest_file = 'registration/' + os.path.basename(dest)
        image = ImageFieldFile(
            instance=instance, field=FileField(), name=dest_file)
    except:
        print('bla')
    if created:
        try:
            UserProfile.objects.create(user=instance, phone_number=phone_number,
                                       country=country, address=address, image=image)
        except:
            UserProfile.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
from random import randint
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @classmethod
    def get_user_by_id(cls, id):
        return cls.objects.get(pk=id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def update_filename(instance, fname):
    path = "uploads/"
    time_now = str(datetime.now()).split('.')[0]
    owner = str(instance.owner_id)

    formatting = owner + '_' + time_now + '_' + fname

    return os.path.join(path, formatting)


class Uploads(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image_identifier = models.AutoField(primary_key=True)
    title = models.TextField()
    image = models.ImageField(upload_to=update_filename)

    def __str__(self):
        return self.title

    @classmethod
    def get_id_excluded_upload_count(cls, id):
        return cls.objects.exclude(owner=id).count()

    @classmethod
    def get_id_excluded_random_upload(cls, id, count):
        return cls.objects.exclude(owner=id)[randint(0, count - 1)]

    @classmethod
    def get_single_upload_by_id(cls, id):
        return cls.objects.filter(image_identifier=id)[0]

    @classmethod
    def delete_single_upload_by_id(cls, id):
        return cls.objects.filter(image_identifier=id)[0].delete()


class Upvotes(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    upvoter = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='upload_upvoter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)

    @classmethod
    def new_upvotes_instance(cls, upvoter, photo, owner):
        return Upvotes(upvoter=upvoter,
                       photo=photo,
                       owner=owner)

    @classmethod
    def get_upvotes_object(cls, upvoter, photo, owner):
        return cls.objects.filter(upvoter=upvoter,
                                  photo=photo,
                                  owner=owner)

    @classmethod
    def delete_upvotes_object(cls, upvoter, photo, owner):
        return cls.get_upvotes_object(upvoter=upvoter,
                                      photo=photo,
                                      owner=owner).delete()


class Downvotes(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    downvoter = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='upload_downvoter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)

    @classmethod
    def new_downvotes_instance(cls, downvoter, photo, owner):
        return Downvotes(downvoter=downvoter,
                         photo=photo,
                         owner=owner)

    @classmethod
    def get_downvotes_object(cls, downvoter, photo, owner):
        return cls.objects.filter(downvoter=downvoter,
                                  photo=photo,
                                  owner=owner)

    @classmethod
    def delete_downvotes_object(cls, downvoter, photo, owner):
        return cls.get_downvotes_object(downvoter=downvoter,
                                        photo=photo,
                                        owner=owner).delete()


class Favorites(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    favoriter = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='upload_favoriter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)

    @classmethod
    def new_favorites_instance(cls, favoriter, photo, owner):
        return Favorites(favoriter=favoriter,
                         photo=photo,
                         owner=owner)

    @classmethod
    def get_favorites_object(cls, favoriter, photo, owner):
        return cls.objects.filter(favoriter=favoriter,
                                  photo=photo,
                                  owner=owner)

    @classmethod
    def delete_favorites_object(cls, favoriter, photo, owner):
        return cls.get_favorites_object(favoriter=favoriter,
                                        photo=photo,
                                        owner=owner).delete()

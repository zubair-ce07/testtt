from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.TextField(blank=True)
    city = models.CharField(max_length=200)
    state_province = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50)
    twitter = models.CharField(max_length=200, blank=True)
    linkedIn = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    brief_description = models.TextField(default="")
    is_public = models.BooleanField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    company_name = models.CharField(max_length=500, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    currently_working_here = models.BooleanField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=300)
    school_location = models.CharField(max_length=500, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    degree = models.CharField(max_length=500)
    field_of_study = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    currently_attending_here = models.BooleanField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class BookMarkCV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_bookmarked_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

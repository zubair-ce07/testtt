from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from phone_field import PhoneField


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True, default=SET_NULL)
    phone = PhoneField(blank=True, )
    address = models.TextField()


class WorkInformation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)
    job_location = models.CharField(max_length=50)
    company = models.CharField(max_length=30)
    joining_date = models.DateField(auto_now=True)
    leaving_date = models.DateField(default='')
    status = models.BooleanField(default=True)


class AcademicInformation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institution_type = models.CharField(
        choices=(('School', 'School'), ('College', 'College'), ('University', 'University')),
        max_length=20,
        error_messages={'invalid_choice ': "Invalid choice of academic institution"})
    institution_name = models.CharField(max_length=50)
    degree_type = models.CharField(max_length=20,
                                   choices=(('Under Graduate', 'Under Graduate'), ('Post Graduate', 'Post Graduate')),
                                   error_messages={'invalid_choice': 'Invalid choice of degree type'})
    start_date = models.DateField(default='')
    end_date = models.DateField(default='')


class Friends(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2')
    close_friend = models.BooleanField(default=False)

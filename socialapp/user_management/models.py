from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL
from phone_field import PhoneField


class SocialGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(User):
    date_of_birth = models.DateField()
    phone = PhoneField(blank=True, )
    address = models.TextField()

    social_groups = models.ManyToManyField(SocialGroup, blank=True, default=SET_NULL, symmetrical=True,
                                           through='UserGroup')
    friends = models.ManyToManyField('self', through='Friend', symmetrical=False, related_name='user_friends')

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(SocialGroup, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


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


class Friend(models.Model):
    user_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_to')
    user_from = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_from')
    close_friend = models.BooleanField(default=False)


class FriendRequest(models.Model):
    request_from = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='request_from')
    request_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='request_to')
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('request_from', 'request_to', )


class GroupRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='member')
    group = models.ForeignKey(SocialGroup, on_delete=models.CASCADE, related_name='associated_group')
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'group', )


class Notification(models.Model):
    text = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, )

from django.db import models


class User(models.Model):
    """ Conatins attributes of User model """
    username = models.CharField(max_length=120, unique=True, blank=False, null=False)
    password = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # every time
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

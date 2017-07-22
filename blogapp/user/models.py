from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, error_messages={'error': 'Invalid Gender'}, blank=True)
    image = models.ImageField(upload_to='user-images', default='user.png', blank=True)
    created_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.user.username

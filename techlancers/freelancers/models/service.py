from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objective = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_service(sender, instance, created, **kwargs):
    if created:
        for i in range(0, 6):
            service = Service.objects.create(user=instance)
            service.save()

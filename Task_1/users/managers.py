from django.db import models


class UserProfileManager(models.Manager):
    def active_list(self):
        return self.filter(user__is_active=True)

    def inactive_list(self):
        return self.filter(user__is_active=False)

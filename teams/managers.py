from django.db import models


class SoftDeleteManager(models.Manager):
    """ Use this manager to get objects that have a deleted field """
    def get_query_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(is_active=True)

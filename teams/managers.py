from django.db import models


class NonTrashManager(models.Manager):
    """ Query only objects which have not been trashed. """
    def get_query_set(self):
        query_set = super(NonTrashManager, self).get_query_set()
        return query_set.filter(trashed_at__isnull=True)


class TrashManager(models.Manager):
    """ Query only objects which have been trashed. """
    def get_query_set(self):
        query_set = super(TrashManager, self).get_query_set()
        return query_set.filter(trashed_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """ Use this manager to get objects that have a deleted field """
    def get_query_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(deleted=False)

    def all_with_deleted(self):
        return super(SoftDeleteManager, self).get_query_set()

    def deleted_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(deleted=True)

    def get(self, *args, **kwargs):
        """ if a specific record was requested, return it even if it's deleted """
        return self.all_with_deleted().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """ if pk was specified as a kwarg, return even if it's deleted """
        if 'pk' in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)
        return self.get_query_set().filter(*args, **kwargs)

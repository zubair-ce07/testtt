from django.db import models
from twitter.models import User


class NewsManager(models.Manager):
    def truncate(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM "{0}"'.format(self.model._meta.db_table))
            cursor.execute('VACUUM;')


class News(models.Model):
    title = models.CharField(max_length=200)
    content =  models.CharField(max_length=1000)
    publisher =models.ForeignKey(User, blank=True, null=True)
    pub_date = models.DateTimeField('published date', auto_now_add=True)
    image = models.ImageField(null=True)
    image_url = models.URLField(null=True)
    objects = NewsManager()

    class Meta:
        ordering = ('-pub_date',)
        db_table = 'news'

    def __str__(self):
        return self.title

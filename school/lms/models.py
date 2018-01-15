from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return '%s' % (self.name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    issued_to = models.ManyToManyField('auth.User', related_name='book_issue', through='Bookissue')


class Bookissue(models.Model):
    user = models.ForeignKey('auth.User', related_name='users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='books')
    issue_date = models.DateTimeField()
    returned_date = models.DateTimeField()


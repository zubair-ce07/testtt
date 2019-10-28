from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author_name = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    number_of_books = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="book_issue")
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

class IssueBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False,  on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=False, null=False,  on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    issue_date = models.DateField(blank=False, null=False)
    return_date = models.DateField(blank=False, null=False)

    def __unicode__(self):
        return '%s issued by %s' % (self.title, self.user.username)

    def get_absolute_url(self):
        return reverse('issuebook_detail', kwargs={'ik': self.ik})
    
    class Meta:
        get_latest_by = "issue_date"
        ordering = ['title']
        verbose_name = "book"
        verbose_name_plural = "books"

class RequestBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False,  on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=False, null=False,  on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    issue_date = models.DateField(blank=False, null=False)
    return_date = models.DateField(blank=False, null=False)

    def __unicode__(self):
        return '%s issued by %s' % (self.title, self.user.username)

    def get_absolute_url(self):
        return reverse('user_requests_detail', kwargs={'ik': self.ik})
    
    class Meta:
        get_latest_by = "issue_date"
        ordering = ['title']
        verbose_name = "book_request"
        verbose_name_plural = "books_requests"



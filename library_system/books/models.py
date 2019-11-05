"""Module for books app models."""
from django.db import models
from django.conf import settings
from django.urls import reverse


class Book(models.Model):
    """Class model for Book."""

    title = models.CharField(max_length=100, unique=True)
    author_name = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    number_of_books = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

class IssueBook(models.Model):
    """Class model for Book Issuing by user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(blank=False, null=False)
    return_date = models.DateField(blank=False, null=False)


    class Meta:
        """Meta class for Issuing Book model."""

        get_latest_by = "issue_date"
        ordering = ['book']
        verbose_name = "book"
        verbose_name_plural = "books"

class RequestBook(models.Model):
    """Class model for Book Requests by user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(blank=False, null=False)
    return_date = models.DateField(blank=False, null=False)


    class Meta:
        """Meta class for Requesting Book model."""

        get_latest_by = "issue_date"
        ordering = ['book']
        verbose_name = "book_request"
        verbose_name_plural = "books_requests"

import uuid
from datetime import date

from django.db import models
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User

from catalog.choices import BookInstanceLoanChoices


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def clean(self):
        if self.date_of_death < self.date_of_birth:
            raise forms.ValidationError('Date of Death should come after Date of Birth')

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the book's natural language)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='13 Character <a href = "https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Select genres for this book')
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=1, choices=BookInstanceLoanChoices.Choices,
                              blank=True, default='d', help_text='Book availability')
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        return '{}({})'.format(self.id, self.book.title)

    @property
    def is_overdue(self):
        return True if self.due_back and date.today() > self.due_back else False

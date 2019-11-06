from django.db import models
from django.urls import reverse
from django.utils import timezone

from .author import Author
from .category import Category
from .publisher import Publisher


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    publisher = models.ForeignKey(Publisher, null=True, related_name='books',
                                  on_delete=models.SET_NULL)

    date_published = models.DateTimeField(default=timezone.now)
    isbn = models.CharField(db_index=True, max_length=13, unique=True,
                            default=None)
    pages = models.PositiveIntegerField(default=1)
    title = models.CharField(db_index=True, max_length=200, default=None)

    class Meta:
        ordering = ['title',]

    def display_categories(self):
        """Creates a string for the Category."""
        return ', '.join([category.name for category in self.categories.all()])
    display_categories.short_description = 'Category'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

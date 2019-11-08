import logging

from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ..apps import LibraryApiConfig
from ..utils import list_diff, list_intersection
from .author import Author
from .category import Category
from .publisher import Publisher

logger = logging.getLogger(__name__)


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    publisher = models.ForeignKey(Publisher,
                                  null=True,
                                  related_name='books',
                                  on_delete=models.SET_NULL)

    date_published = models.DateTimeField(default=timezone.now)
    isbn = models.CharField(db_index=True,
                            max_length=13,
                            unique=True,
                            default=None)
    pages = models.PositiveIntegerField(default=1)
    title = models.CharField(db_index=True, max_length=200, default=None)

    class Meta:
        ordering = ['title',]

    def display_categories(self):
        """Creates a string for the Category."""
        return ', '.join([category.name for category in self.categories.all()])

    display_categories.short_description = 'Categories'

    def display_authors(self):
        """Creates a string for the Authors."""
        return ', '.join([author.first_name for author in self.authors.all()])

    display_authors.short_description = 'Authors'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def inspect(self):
        return self.__dict__

    @staticmethod
    def update_m2m(given_models, actual_model):
        model_name = actual_model.model.__name__
        app_name = LibraryApiConfig.name
        model_klass = apps.get_model(app_name, model_name)

        existing_ids = list(actual_model.values_list('pk', flat=True))
        try:
            given_ids = [model['id'] for model in given_models]
        except KeyError:
            logger.err(f"{model_name} id: {id} id not found in author object")

        keep = list_intersection(existing_ids, given_ids)
        delete_ids = list_diff(existing_ids, keep)
        add_ids = list_diff(given_ids, keep)

        # Add new assocations
        models = model_klass.objects.filter(id__in=add_ids)
        if models:
            actual_model.add(*models)

        # Remove old assocations
        models = []
        models = model_klass.objects.filter(id__in=delete_ids)
        if models:
            actual_model.remove(*models)

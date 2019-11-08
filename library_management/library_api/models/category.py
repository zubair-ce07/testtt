from django.db import models


class Category(models.Model):
    """Model representing a book category (e.g. Adeventure, Non Fiction)."""
    name = models.CharField(default=None, max_length=200)

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = "Categories"

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def inspect(self):
        return self.__dict__

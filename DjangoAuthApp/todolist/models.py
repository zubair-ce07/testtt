from django.db import models

from django.utils import timezone


class TodoList(models.Model):  # Todolist able name that inherits models.Model
    title = models.CharField(max_length=250)  # a varchar
    content = models.TextField(blank=True)  # a text field
    created = models.DateField(auto_now_add=True)  # a date
    created.editable = True

    due_date = models.DateField(default=timezone.now)  # a date

    class Meta:
        ordering = ["-created"]  # ordering by the created field

    def __str__(self):
        return self.title  # name to be shown when called

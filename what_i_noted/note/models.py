from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class NoteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=150, blank=True)
    publisher_name = models.CharField(max_length=150, blank=True)
    published_date = models.DateField(default=timezone.now, blank=True)
    isbn = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(default='default_note_thumb.png', upload_to='note_book_thumbnails')
    thumbnail_url = models.CharField(max_length=5000, blank=True)
    is_public = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Note(models.Model):
    note_book = models.ForeignKey(NoteBook, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = HTMLField()
    tags = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(default='default_note_image.png', upload_to='note_book_thumbnails')
    is_public = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

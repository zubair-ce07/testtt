from django.db import models
from django.contrib.auth.models import User

class Website(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    full_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    TECH = 'Technology'
    BUSINESS = 'Business'
    SPORTS = 'Sports'
    EDUCATION = 'Education'
    SCIENCE = 'Science'
    INTERNATIONAL = 'International'
    ENTERTAINMENT = 'Entertainment'
    LIFESTYLE = 'Lifestyle'
    MISC = 'Miscellaneous'

    title = models.CharField(max_length=300)
    category = models.CharField(
        max_length=13,
        choices=[
            (TECH, TECH),
            (BUSINESS, BUSINESS),
            (SPORTS, SPORTS),
            (EDUCATION, EDUCATION),
            (SCIENCE, SCIENCE),
            (INTERNATIONAL, INTERNATIONAL),
            (ENTERTAINMENT, ENTERTAINMENT),
            (LIFESTYLE, LIFESTYLE),
            (MISC, MISC)
        ],
        default=MISC
    )
    authors = models.ManyToManyField(Author, related_name='authors')
    website = models.ForeignKey(Website, related_name='website', on_delete=models.DO_NOTHING)
    image_url = models.URLField(max_length=1000)
    content = models.TextField()
    publish_time = models.DateTimeField()
    url = models.URLField(max_length=400, unique=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="article_comments", on_delete=models.DO_NOTHING)
    comment_text = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments", on_delete=models.DO_NOTHING)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

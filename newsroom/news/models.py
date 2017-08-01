from django.db import models
from categories.models import Category

class Newspaper(models.Model):
    name = models.CharField(max_length=50)
    source_url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Scrapper(models.Model):
    name = models.CharField(unique=True, max_length=50)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class NewsSource(models.Model):
    name = models.CharField(unique=True, max_length=60)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.TextField()
    published_date = models.DateField()
    scraped_date = models.DateField(auto_now_add=True)
    source_url = models.URLField(unique=True)
    image_url = models.URLField()
    abstract = models.TextField()
    detail = models.TextField()
    summary = models.TextField(null=True, blank=True)
    news_source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return "{} | {}".format(self.title, str(self.published_date))

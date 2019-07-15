from django.db import models

class Website(models.Model):
    website_name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, unique=True)

    def __str__(self):
        return self.website_name

class Author(models.Model):
    full_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.full_name

class Category(modesl.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Article(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, related_name='authors', on_delete=models.CASCADE)
    website = models.ForeignKey(Website, related_name='website', on_delete=models.CASCADE)
    content = models.TextField()
    publish_time = models.DateTimeField()
    url = models.URLField(max_length=400, unique=True)

    def __str__(self):
        return self.title

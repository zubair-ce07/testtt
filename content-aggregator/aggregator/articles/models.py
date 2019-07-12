from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.address

class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    num_of_articles = models.IntegerField()

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=50)
    authors = models.ArrayField(
        models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE)
    )
    website = models.ForeignKey(Website, related_name='website', on_delete=models.CASCADE)
    body = models.TextField(max_length=4000)
    publish_time = models.DateTimeField('date published')
    url = models.URLField(max_length=400)

    def __str__(self):
        return self.title

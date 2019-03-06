from django.db import models


class Trends(models.Model):
    trend_link = models.CharField(max_length=200)
    title = models.TextField()
    image_link = models.CharField(max_length=200)


class Tweets(models.Model):
    # id = models.IntegerField(primary_key=True)
    profile_image = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    tweet_data = models.TextField()
    trend = models.ForeignKey(Trends, on_delete=models.CASCADE, related_name='tweets')

    def __str__(self):
        return self.username


from django.db import models

from accounts.models import User
from seller.models import Category


class Requests(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    date = models.TextField(max_length=200)
    duration = models.IntegerField()  # Num of Days
    budget = models.IntegerField()  # integer Dollars
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


def buyer_request_files_path(instance, filename):
    """
        returns the path where the
        gig gallery images should be stored
    """
    return "files/requests/{0}_{1}_{2}".format(
        instance.request.id,
        instance.request.buyer.username,
        filename
    )


class RequestFiles(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    file_name = models.FileField(upload_to=buyer_request_files_path)

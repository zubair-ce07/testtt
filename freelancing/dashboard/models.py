from django.db import models

from accounts.models import User
from seller.models import Category, Gig


class Requests(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    date = models.TextField(max_length=200)
    duration = models.IntegerField()  # Num of Days
    budget = models.IntegerField()  # integer Dollars
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = "Requests"


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
    request = models.ForeignKey(
        Requests,
        on_delete=models.CASCADE,
        related_name="request_files"
    )
    file_name = models.FileField(
        upload_to=buyer_request_files_path,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Request Files"


class Offers(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    buyer_request = models.ForeignKey(Requests, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=1000)
    offer_amount = models.IntegerField()
    delivery_time = models.IntegerField()
    revisions = models.IntegerField()

    class Meta:
        unique_together = (('gig', 'buyer_request'),)

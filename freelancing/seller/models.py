from django.db import models
from accounts.models import User


class Category(models.Model):
    category_name = models.TextField(max_length=100)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "categories"


class SearchTag(models.Model):
    search_tag = models.TextField(max_length=100)

    class Meta:
        db_table = 'search_tags'


class Gig(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    gig_title = models.TextField(max_length=300)
    description = models.TextField(max_length=1000)
    categories = models.ManyToManyField(Category)
    search_tags = models.ManyToManyField(SearchTag)


class Package(models.Model):
    gig = models.ForeignKey(
        Gig,
        related_name="gig_packages",
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=100)
    details_offering = models.TextField(max_length=300)
    delivery_time = models.IntegerField()  # Num of Days
    revisions = models.IntegerField()
    price = models.IntegerField()  # only integer dollars


class Faq(models.Model):
    gig = models.ForeignKey(
        Gig,
        on_delete=models.CASCADE,
        related_name="gig_faqs",
    )
    question = models.TextField(max_length=400)
    answer = models.TextField(max_length=400)


class Requirements(models.Model):
    gig = models.ForeignKey(
        Gig,
        on_delete=models.CASCADE,
        related_name="gig_requirements",
    )
    requirement_text = models.TextField(max_length=500)


def gig_gallery_images_path(instance, filename):
    """
        returns the path where the
        gig gallery images should be stored
    """
    return "images/gigs/gallery/{0}_{1}_{2}".format(
        instance.gig.id,
        instance.gig.gig_title,
        filename
    )


class Gallery(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    gig_image = models.ImageField(upload_to=gig_gallery_images_path)

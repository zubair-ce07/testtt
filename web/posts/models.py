from django.db import models
from django.utils import timezone

from web.users.models import Address


class Post(models.Model):

    KIND_CHOICES = [('house', 'House'), ('plot', 'Plot'),
                    ('commercial_plot', 'Commercial Plot'), ('commercial_building', 'Commercial Building'),
                    ('flat', 'Flat'), ('shop', 'Shop'), ('farm_house', 'Farm House'), ]

    posted_by = models.ForeignKey('users.User', related_name='posts')
    title = models.CharField(max_length=255)
    area = models.DecimalField(decimal_places=3, max_digits=100)
    location = models.OneToOneField(Address)

    description = models.TextField(max_length=1024)

    kind = models.CharField(max_length=255, choices=KIND_CHOICES)
    contact_number = models.CharField(max_length=255)
    demanded_price = models.DecimalField(decimal_places=3, max_digits=100)
    is_sold = models.BooleanField(default=False)

    sold_on = models.DateTimeField(blank=True, null=True)
    posted_on = models.DateTimeField(default=timezone.now)
    expired_on = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    @property
    def number_of_views(self):
        return self.post_views.all().count()

    # TODO: As we already know this is related to Post, no need to add post in the property name
    @property
    def is_post_expired(self):
        if not self.is_expired:
            #TODO: DON'T REMOVE THIS ONE...That's not the right way to do things like this, use the background process instead. Leave it as is for now.
            time_delta = self.expired_on - timezone.now()
            if time_delta.total_seconds() < 0:
                self.is_expired = True
                self.save()
        return self.is_expired

    @property
    def time_until_expired(self):
        days_hours_minutes_dict = None
        time_delta = self.expired_on - timezone.now()
        days, hours, minutes = time_delta.days, time_delta.seconds // 3600, time_delta.seconds // 60 % 60
        if days > 0:
            days_hours_minutes_dict = dict(days=days, hours=hours, minutes=minutes)
        return days_hours_minutes_dict


class Request(models.Model):
    STATUS_CHOICES = [('pending', 'pending'), ('rejected', 'rejected'),
                      ('accepted', 'accepted')]

    requested_by = models.ForeignKey('users.User', related_name='requests')
    post = models.ForeignKey('Post', related_name='requests')
    message = models.CharField(max_length=512)
    price = models.DecimalField(decimal_places=3, max_digits=100)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    requested_on = models.DateTimeField(default=timezone.now)


class PostView(models.Model):
    viewed_by = models.ForeignKey('users.User', related_name='views')
    post_viewed = models.ForeignKey('posts.Post', related_name='post_views')
    viewed_on = models.DateTimeField(default=timezone.now)






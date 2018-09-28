import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    """
    Tag model
    """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BallotManager(models.Manager):
    """
    Ballot model manager
    """

    def get_active_ballots(self):
        """Return all ordered active ballot"""
        return self.filter(is_active=True).order_by('-created_at')


class Ballot(models.Model):
    """
    Ballot model
    """
    title = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    ending_date = models.DateTimeField(null=True, blank=True)
    active_period = models.IntegerField(
        help_text="Number of days a Ballot should remain active", default=3,
        validators=[MaxValueValidator(30), MinValueValidator(3)]
    )
    tags = models.ManyToManyField(Tag)
    is_active = models.BooleanField(default=True)
    objects = BallotManager()

    def __str__(self):
        return self.title

    @property
    def choices(self):
        """
        Provides choice sets of Ballot
        :return: choice set.
        """
        return self.choice_set.all()

    @property
    def votes_casted(self):
        """
        Provides choice sets of Ballot
        :return: choice set.
        """
        total_casted_votes = sum(choice.votes for choice in self.choices)
        return total_casted_votes

    @property
    def should_remain_active(self) -> bool:
        """
        Returns if a ballot deadline has come/passed recently
        :return: False if it should not be active else True
        """
        return timezone.now() < self.ending_date

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.ending_date = timezone.now() + datetime.timedelta(days=self.active_period)
        super().save(force_insert, force_update, using, update_fields)


class Choice(models.Model):
    """
    Choice model
    """
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def votes(self):
        """
        Provides vote counts.
        :return: Votes
        """
        return self.vote_set.count()


class Vote(models.Model):
    """
    Vote model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')

    def __str__(self):
        return '{0}-{1}'.format(self.user.first_name, self.choice.text)

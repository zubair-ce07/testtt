from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Task(models.Model):
    """
    Model for tasks that are needed to be completed
    to eliminate safety threats.
    """

    PENDING = 0
    STARTED = 1
    COMPLETED = 2

    STATUSES = (
        (PENDING, 'Pending'),
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
    )

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITIES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUSES, default=PENDING)
    priority = models.PositiveSmallIntegerField(choices=PRIORITIES)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(get_user_model())

    def is_completed(self):
        return True if self.status == self.COMPLETED else False
    is_completed.boolean = True


class Investigation(models.Model):
    """
    investigation into reports whether these reports
    are correct or not. It is to learn about GenericForeignKey
    """
    is_correct = models.BooleanField()
    investigated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class SafetyHazard(models.Model):
    """
    This model houses any reports that indicate
    a safety threat. and has a related task to
    eliminate that threat.
    """
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    desc = models.TextField()
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reported_at = models.DateTimeField(default=timezone.now)
    investigations = GenericRelation(Investigation, related_query_name='hazard')


class SafeActReport(models.Model):
    """
    Model for reports that are informing about
    acts that improve safety.
    """
    remarks = models.TextField()
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reported_at = models.DateTimeField(default=timezone.now)
    investigations = GenericRelation(Investigation, related_query_name='report')


class Movie(models.Model):
    """
    A simple movie model consisting of title and owners but in
    method for string representation initiate db queries on related models
    Used to learn query optimization by using prefetch related
    """
    title = models.CharField(max_length=100)
    owners = models.ManyToManyField(get_user_model(), related_name='owned_movies')

    def __str__(self):
        return '{title} ({owners})'.format(
            title=self.title,
            owners=', '.join(owner.email for owner in self.owners.all())
        )

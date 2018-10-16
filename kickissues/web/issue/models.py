from django.contrib.auth.models import User
from django.db import models


class PriorityType:
    HIGH = 'high'
    NORMAL = 'normal'
    LOW = 'low'

    CHOICES = (
        (HIGH, HIGH),
        (NORMAL, NORMAL),
        (LOW, LOW)
    )


class StatusChoices:
    TODO = 'todo'
    REVIEW = 'review'
    RESOLVED = 'resolved'

    CHOICES = (
        (TODO, TODO),
        (REVIEW, REVIEW),
        (RESOLVED, RESOLVED)
    )


class Issue(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PriorityType.CHOICES, default=PriorityType.LOW)
    status = models.CharField(max_length=20, default=StatusChoices.TODO, choices=StatusChoices.CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    manage_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='assigned_issues'
    )
    edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    assigned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, editable=False, default=None)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.comment

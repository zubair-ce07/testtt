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


class Issue(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='issues')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PriorityType.CHOICES, default=PriorityType.LOW)
    status = models.CharField(max_length=20, default="todo")
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    manage_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        related_name='assigned_issues'
    )
    last_edit = models.DateTimeField(auto_now=True, blank=True, null=True)
    resolved_date = models.DateTimeField(blank=True, null=True)
    assigned_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, blank=False, null=False)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    comment = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.comment

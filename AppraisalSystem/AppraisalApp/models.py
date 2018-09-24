from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404, Http404

COMPETENCY_RANGE = [MaxValueValidator(10), MinValueValidator(1)]
USER_TYPES = [("CEO", "CEO"), ("Manager", "Manager"), ("Worker", "Worker"), ]


class Employee(AbstractUser):
    employee_type = models.CharField(max_length=10, choices=USER_TYPES, blank=True, default="Worker")
    reports_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Employee'

    def get_record(employee_id, manager_id):
        employee = get_object_or_404(Employee, pk=employee_id)
        manager = get_object_or_404(Employee, pk=manager_id)

        if employee.reports_to == manager or manager.employee_type == "CEO":
            return employee
        return Http404


class Feedback(models.Model):
    from_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='given_feedbacks')
    to_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedbacks')
    publishing_date = models.DateTimeField(auto_now_add=True)

    def get_record(fb_id, fb_from):
        fb = get_object_or_404(Feedback, pk=fb_id)

        if fb.from_user == fb_from:
            return fb
        return Http404

    def get_to_user_id(fb_id):
        fb = get_object_or_404(Feedback, pk=fb_id)
        if fb:
            return fb.to_user.id
        return Http404


class Competency(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, unique=True)
    comment = models.TextField(max_length=500, blank=True)
    team_work = models.IntegerField(default=1, validators=COMPETENCY_RANGE)
    leadership = models.IntegerField(default=1, validators=COMPETENCY_RANGE)

    def get_record(fb_id):
        feedback_ = get_object_or_404(Feedback, pk=fb_id)
        competency = get_object_or_404(Competency, feedback=feedback_)
        return competency

    def save_form(from_user, to_user, form):
        feedback = Feedback()
        feedback.from_user = from_user
        feedback.to_user = get_object_or_404(Employee, pk=to_user)
        feedback.save()

        competency = Competency()
        competency.feedback = feedback
        competency.comment = form.cleaned_data.get('comment')
        competency.team_work = form.cleaned_data.get('team_work')
        competency.leadership = form.cleaned_data.get('leadership')
        competency.save()

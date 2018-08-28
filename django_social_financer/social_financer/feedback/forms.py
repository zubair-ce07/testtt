__author__ = 'abdul'
from django.forms import ModelForm

from .models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ['given_by_user', 'given_to_user', 'date_logged']

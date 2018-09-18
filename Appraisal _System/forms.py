
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.http import request

from .models import Appraisal

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'title', 'department', 'report_to' )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['report_to'].queryset = User.objects.filter(Q(user_level="manager") | Q(user_level="admin"))


class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields=('description', 'comment', 'to_user', 'from_user')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 25}),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 26}),
            'from_user': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)
        super(AppraisalForm, self).__init__(*args, **kwargs)
        self.fields['to_user'].queryset = User.objects.filter(report_to=manager)


class ExtendedAppraisalForm(AppraisalForm):
    decision_making = forms.IntegerField(min_value=1, max_value=10, required=True)
    confidence = forms.IntegerField(min_value=1, max_value=10, required=True)
    problem_solving = forms.IntegerField(min_value=1, max_value=10, required=True)

    class Meta(AppraisalForm.Meta):
        fields = AppraisalForm.Meta.fields + ('decision_making', 'confidence', 'problem_solving')
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Appraisal, Competence


User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'title', 'department')


class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = ('description', 'comment', 'to_user', 'from_user')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 25}),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 26}),
        }

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)
        super(AppraisalForm, self).__init__(*args, **kwargs)
        self.fields['from_user'].queryset = User.objects.filter(pk=manager.pk)
        self.fields['to_user'].queryset = User.objects.filter(
            report_to=manager)


class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = ('decision_making', 'confidence', 'problem_solving')

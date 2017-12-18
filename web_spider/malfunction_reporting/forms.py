from django import forms
from django.contrib.auth import get_user_model
from malfunction_reporting.models import SafetyHazard, Task


class SafetyHazardForm(forms.ModelForm):
    """
    form to allowing user create new reports on safety threats that involve
    creating new tasks to eliminate those threats
    """
    priority = forms.ChoiceField(choices=Task.PRIORITIES)
    assignee = forms.ModelChoiceField(queryset=get_user_model().objects.all())

    class Meta:
        model = SafetyHazard
        fields = ('priority', 'assignee', 'desc',)

    def save(self, commit=True, request=None):
        hazard = super(SafetyHazardForm, self).save(commit=False)
        self.cleaned_data.pop('desc')
        task = Task.objects.create(**self.cleaned_data)
        hazard.task = task
        hazard.reported_by = request.user
        hazard.save()
        return hazard

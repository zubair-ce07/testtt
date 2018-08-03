from datetime import date
from django import forms

from taskmanager.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assignee', 'description', 'due_date']
        widgets = {
            'due_date':    forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"))
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assignee'].initial = user

    def clean(self):
        """ Checks if the due date entered is correct """
        due_date = self.cleaned_data['due_date']
        delta = due_date - date.today()
        if delta.days < 0:
            raise forms.ValidationError(u"The due date cannot be prior to today !")
        return self.cleaned_data

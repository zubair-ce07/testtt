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
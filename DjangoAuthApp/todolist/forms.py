from django import forms

from .models import TodoList


class TodoAddForm(forms.ModelForm):
    due_date = forms.DateField(required=False, help_text='Optional.', widget=forms.DateInput(
        attrs={'class': 'taskDate', 'id': 'dueDate', 'type': 'date'}))

    class Meta:
        model = TodoList
        fields = ['title', 'due_date']

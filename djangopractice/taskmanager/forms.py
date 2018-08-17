from datetime import date, datetime, timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm

from taskmanager.models import CustomUser, Task


class TaskForm(forms.ModelForm):
    status_choice = (('0', 'In Progress'), ('1', 'Completed'))
    due_date = forms.fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                      initial=datetime.now()+timedelta(days=7))
    status = forms.fields.ChoiceField(required=True, choices=status_choice)

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'assignee', 'description', 'status', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assignee'].initial = user
        self.fields['status'].initial = 0


class AddTaskForm(TaskForm):

    def clean(self):
        """ Checks if the due date entered is correct """
        due_date = self.cleaned_data['due_date']
        delta = due_date - date.today()
        if delta.days < 0:
            raise forms.ValidationError(u"The due date cannot be prior to today !")
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
                self.fields[field_name].help_text = None


class CustomUserChangeForm(forms.ModelForm):
    birth_date = forms.fields.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    image = forms.fields.ImageField(label='Change Image',
                                    required=False, widget=forms.widgets.FileInput(attrs={'type': 'file'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'birth_date', 'image']

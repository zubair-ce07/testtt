from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Task


class CustomUserSignupForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'profile_picture', 'city', 'email']


class LoginForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'profile_picture']

    def save(self, commit=True):
        user_form = super(UpdateProfileForm, self).save(commit=False)
        user = CustomUser.objects.get(pk=user_form.pk)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.city = self.cleaned_data["city"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.save()
        return user


class UpdateTaskForm(forms.Form):
    status = forms.BooleanField(required=False)


class AddTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'user', 'status', 'dated']
        widgets = {
            'dated': forms.DateInput(attrs={'class': 'datepicker'}),
        }
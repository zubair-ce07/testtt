from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class SigninForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class StatusForm(forms.Form):
    status = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Share yor thoughts'}))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    GENDER_CHOICES = (
        ('Male', u"Male"),
        ('Female', u"Female"),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    date_of_birth = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'datepicker'}))

    def _add_user(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password']
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name)
        user.set_password(password)

        user.save()
        return user

    def save(self, commit=True):
        if commit:
            user = self._add_user()
            date_of_birth = self.cleaned_data['date_of_birth']
            gender = self.cleaned_data['gender']
            user_profile = UserProfile.objects.get(user=user)
            user_profile.date_of_birth = date_of_birth
            user_profile.gender = gender
            user_profile.save()

        return self

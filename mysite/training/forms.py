from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
from .signals import add_trainee_signal, add_trainer_signal


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SignUpForm(forms.Form):

    class Media:
        js = ('js/validations.js',
              'https://code.jquery.com/jquery-3.1.0.min.js')

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username',
               'onfocusout': "verifyUserName(event)"}))

    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'First Name',
               'onkeypress': 'return verifyName(event)'}))

    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Last Name',
               'onkeypress': 'return verifyName(event)'}))

    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))

    def __update_user_profile(self, user):
        picture = self.cleaned_data['picture']
        user_profile = UserProfile.objects.get(user=user)
        if picture:
            user_profile.picture = picture
        else:
            user_profile.picture = "default.png"

        user_profile.name = user.get_full_name()

        user_profile.save()

    def __add_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name)

        user.set_password(password)
        user.save()
        return user

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get("username")

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return

        raise forms.ValidationError("Username already exists")

    def save(self, account_type, commit=True):
        if commit:
            user = self.__add_user()
            self.__update_user_profile(user)
            """
            Sending Trainer/Trainee Signal to
            to add Trainer/Trainee accordingly
            """
            if account_type == "Trainee":
                add_trainee_signal.send(sender=self.__class__, user=user)
            elif account_type == "Trainer":
                add_trainer_signal.send(sender=self.__class__, user=user)
        return self

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
from .signals import add_trainee_signal, add_trainer_signal


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    picture = forms.ImageField(required=False)

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

    def save(self, account_type, commit=True):
        if commit:
            user = self.__add_user()
            self.__update_user_profile(user)
            if account_type == "Trainee":
                add_trainee_signal.send(sender=self.__class__, user=user)
            elif account_type == "Trainer":
                add_trainer_signal.send(sender=self.__class__, user=user)
        return self
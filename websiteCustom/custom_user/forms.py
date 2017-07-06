from django import forms
from django.shortcuts import get_object_or_404

from .models import CustomUser


class UserRegisterForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'current_address', 'permanent_address', 'password']

    def save(self, commit=True):
        user_form = super(UserUpdateForm, self).save(commit=False)
        user = get_object_or_404(CustomUser, pk=user_form.pk)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        user.current_address = self.cleaned_data["current_address"]
        user.permanent_address = self.cleaned_data["permanent_address"]
        user.save()
        return user

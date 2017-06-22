from django.contrib.auth.models import User
from django import forms


class UserRegisterForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user_form = super(UserUpdateForm, self).save(commit=False)
        user = User.objects.get(id=user_form.pk)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()
        return user

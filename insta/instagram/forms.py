from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea)
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    # avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2', 'bio',)

    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user.set_password(user.password)
    #     if commit:
    #         user.save()
    #     return user

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    #
    # class Meta:
    #     model = User
    #     fields = ('email',)


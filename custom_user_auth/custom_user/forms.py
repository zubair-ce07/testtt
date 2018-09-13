from django import forms
from django.contrib.auth import password_validation
from .models import MyUser


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': "please enter your password", })

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']
        error_messages = {
            'username': {
                'required': "please enter a username",
                'max_length': 'username should be of maximum length of 150'
            },
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={'required': "please enter your username"})
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': "please enter your password"})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'email']
        error_messages = {
            'username': {
                'required': "please enter a username",
                'max_length': "username should be of maximum length of 150"
            },
            'first_name': {
                'max_length': 'firstname should be of maximum length of 40'
            },
            'last_name': {
                'max_length': 'lastname should be of maximum length of 40'
            },
        }


class UserChangePasswordForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'password_incorrect': (
            "Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        error_messages={'required': "old password is required"}
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput,
        error_messages={'required': "new password is required"}
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.PasswordInput,
        error_messages={'required': "confirm password is required"}
    )

    def validate(self, user):
        # old_password = self.cleaned_data["old_password"]
        # if not user.check_password(old_password):
        #     raise forms.ValidationError(
        #         self.error_messages['password_incorrect'],
        #         code='password_incorrect',
        #     )
        #     # return False
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
                # return False
        password_validation.validate_password(password2, user)
        return password2

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # password_validation.validate_password(password2, self.user)
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

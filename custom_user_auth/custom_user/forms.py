from django import forms
from django.contrib.auth import password_validation
from .models import MyUser



class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'email']


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
        label=("Old password"),
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.PasswordInput,
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



from django import forms


class UserSignUpInForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)


class UserEditProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    qualification = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)

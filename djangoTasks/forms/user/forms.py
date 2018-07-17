"""This module contains Django Forms"""
import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms.models import modelformset_factory

from forms.messages import ErrorMessages
from user.models import UserProfile, Product
from forms.custom_exceptions import InvalidNameInputError

USER = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Class for Registration form, extended from ModelForm for user's model"""
    GENDER_CHOICE = (
        ("", "Select Gender"),
        ("m", "Male"),
        ("f", "Female")
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput()
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICE)

    class Meta:
        model = USER
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password', 'gender'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        """
        raises Validation error if first name contains
        other than alphabets and spaces
        :returns first_name value
        :raises ValidationError
        """
        f_name = self.cleaned_data.get('first_name')
        if re.match('^[a-zA-Z ]+$', f_name):
            return f_name
        raise forms.ValidationError(ErrorMessages.INVALID_NAME_ERROR)

    def clean_last_name(self):
        """
        raises Validation error if last name contains
        other than alphabets and spaces
        :returns last_name value
        :raises ValidationError
        """
        l_name = self.cleaned_data.get('last_name')
        if re.match('^[a-zA-Z ]+$', l_name):
            return l_name
        raise forms.ValidationError(ErrorMessages.INVALID_NAME_ERROR)

    def clean_username(self):
        """
        raises Validation error if username already exists
        :returns username's value
        :raises ValidationError
        """
        username = self.cleaned_data.get('username').lower()
        if USER.objects.filter(username=username).exists():
            raise forms.ValidationError(ErrorMessages.USERNAME_EXISTS)
        return username

    def clean_email(self):
        """
        raises Validation error if email already exists
        :returns email's value
        :raises ValidationError
        """
        email = self.cleaned_data['email'].lower()
        if USER.objects.filter(email=email).exists():
            raise forms.ValidationError(ErrorMessages.EMAIL_EXISTS)
        return email

    def clean_confirm_password(self):
        """
        raises ValidationError if password and confirm password doesn't match
        :return: cleaned password
        :raises ValidationError
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(ErrorMessages.PASSWORD_NOT_MATCHED)
        return confirm_password

    def clean_gender(self):
        """
        raises ValidationError if gender field not selected
        :return: gender's value
        :raises ValidationError
        """
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError(ErrorMessages.GENDER_NOT_SELECTED)
        return gender


class UserProfileForm(forms.ModelForm):
    """UserProfile form class extended from ModelForm for userprofile model"""
    class Meta:
        model = UserProfile
        YEARS = [x for x in range(1940, 2018)]
        fields = ['birthday', 'country', 'state', 'city']
        widgets = {
            'birthday': forms.SelectDateWidget(years=YEARS)
        }


class LoginForm(forms.ModelForm):
    """Login form class extended from ModelForm for user model"""
    current_user = None

    class Meta:
        model = USER
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        """
        check authentication of user with his/her login credentials
        :returns cleaned data
        :raises ValidationError: if authentication fails
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(
                ErrorMessages.INCORRECT_USERNAME_PASSWORD
            )
        self.current_user = user
        return self.cleaned_data


class ProductForm(forms.ModelForm):
    """Product creation form class extended from ModelForm for product model"""
    PRICE_CHOICES = [(x, x) for x in range(10, 1000, 50)]
    price = forms.ChoiceField(choices=PRICE_CHOICES)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


SignUpFormSet = modelformset_factory(UserProfile, exclude=())

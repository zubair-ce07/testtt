from django import forms
from django.forms import ModelForm, Textarea
from memo_app.models import User, Memory
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator, URLValidator


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control separate-form-fields','required': 'required',
                                                 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                            'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'Password', 'type': 'password'}),
        }




class EditProfileForm(SignupForm):
    class Meta(SignupForm.Meta):
        exclude = ('password', )



class LoginForm(forms.Form):
    username = forms.CharField(required=False, label='', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'style':'margin-bottom: 15px;'}))
    password = forms.CharField(required=False, label='', max_length=100, widget=forms.TextInput
                            (attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password', 'style':'margin-bottom: 15px;'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        min_validator = MinLengthValidator(1)
        try:
            min_validator(username)
        except:
            raise forms.ValidationError('Username is not valid')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        min_validator = MinLengthValidator(8)
        max_validator = MaxLengthValidator(100)

        try:
            min_validator(password)
        except:
            raise forms.ValidationError('Enter valid password')

        try:
            max_validator(password)
        except:
            raise forms.ValidationError('Enter valid password')

        return password


class AddMemoForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'text', 'url', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                            'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                          'placeholder': 'Enter detail of the memory'}),
            'url': forms.TextInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                          'placeholder': 'Url'}),
            'tags': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                           'placeholder': 'Comma separated tags'}),
            'image': forms.FileInput(attrs={'class': 'form-control separate-form-fields'}),
        }
        validators = {
            'url': [URLValidator]
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        url_validator = URLValidator()

        try:
            url_validator(url)
        except:
            raise forms.ValidationError('url is not valid')

        return url


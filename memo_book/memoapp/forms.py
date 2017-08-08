from django import forms
from django.forms import ModelForm
from memoapp.models import User, Memory, Category


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                 'placeholder': 'First Name'}),

            'email': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                            'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'User Name'}),
            'password': forms.TextInput( attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'Password', 'type': 'password'}),
        }


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                            'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                               'placeholder': 'Password', 'type': 'password'}),
            'image': forms.FileInput(attrs={'class': 'form-control separate-form-fields'}),
        }

class LoginForm(forms.Form):
    login_email = forms.EmailField(label='', max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                           'placeholder': 'Email'}))
    login_password = forms.CharField(label='', max_length=100, required=False,
                                     widget=forms.TextInput (attrs={'class': 'form-control separate-form-fields',
                                                                    'placeholder': 'Password','type': 'password'}))


class AddMemoForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['category', 'title', 'text', 'url', 'tags', 'is_public', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Enter detail of the memory'}),
            'url': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Url'}),
            'tags': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Comma separated tags'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            
            'is_public': forms.CheckboxInput(attrs={'class': 'input-group '})
        }


class Category(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                           'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control separate-form-fields',
                                          'placeholder': 'Enter description of category'}),
        }


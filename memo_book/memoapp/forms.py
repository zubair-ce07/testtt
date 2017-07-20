from django import forms
from django.forms import ModelForm
from memoapp.models import User, Memory, Category


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password',  'image']
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
            'image': forms.FileInput(attrs={'class': 'form-control separate-form-fields'}),
        }


class EditProfileForm(SignupForm):
    class Meta(SignupForm.Meta):
        exclude = ('password', )


class LoginForm(forms.Form):
    email = forms.EmailField(label='', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                                           'placeholder': 'Email'}))
    password = forms.CharField(label='', max_length=100, widget=forms.TextInput
                            (attrs={'class': 'form-control separate-form-fields', 'placeholder': 'Password',
                                    'type': 'password'}))


class AddMemoForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['category', 'title', 'text', 'url', 'tags', 'is_public', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                            'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                          'placeholder': 'Enter detail of the memory'}),
            'url': forms.URLInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                          'placeholder': 'Url'}),
            'tags': forms.TextInput(attrs={'class': 'form-control separate-form-fields',
                                           'placeholder': 'Comma separated tags'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'image': forms.FileInput(attrs={'class': 'form-control separate-form-fields'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-control separate-form-fields'})
        }


class Category(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                            'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control separate-form-fields', 'required': 'required',
                                          'placeholder': 'Enter description of category'}),
        }


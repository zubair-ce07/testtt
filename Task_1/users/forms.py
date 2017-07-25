from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'label': 'Username', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-group', 'label': 'Password', 'placeholder': 'Password'}))


class EditForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")],
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'Format: +123456789 (Optional)'}))
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs={'class': 'form-control form-group'}),
                                   required=False)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-group'}))
    address = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control form-group', 'placeholder': 'Address (Optional)'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John (Optional)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Doe (Optional)'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }

    def __init__(self, *args, **kwargs):
        self.FILES = kwargs.pop('FILES', None)
        super(EditForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user_profile = self.instance.userprofile
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.address = self.cleaned_data.get('address')
        user_profile.country = self.cleaned_data.get('country')
        if self.FILES.get('image'):
            user_profile.image = self.FILES.get('image')
        elif not self.cleaned_data.get('image'):
            user_profile.image = None
        user_profile.save()
        return super(EditForm, self).save(commit=commit)


class SignupForm(forms.ModelForm):
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'Confirm Password'}))
    phone_number = forms.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")],
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'Format: +123456789 (Optional)'}))
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs={'class': 'form-control form-group'}),
                                   required=False)
    image = forms.ImageField(required=False, label='Diplay Picture',
                             widget=forms.FileInput(attrs={'class': 'form-control form-group'}))
    address = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control form-group', 'placeholder': 'Address (Optional)'}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']

        if password and password2 and password != password2:
            raise forms.ValidationError('The passwords do not match.')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone_number', 'country',
                  'image', 'address')
        labels = {'email': 'Email'}
        help_texts = {'username': None}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-group form-control',
                                                      'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}),
                   'password': forms.PasswordInput(
                       attrs={'class': 'form-control form-group', 'placeholder': 'Enter Password'}),
                   'email': forms.EmailInput(
                       attrs={'class': 'form-group form-control', 'placeholder': 'Email Address', 'required': True}),
                   'first_name': forms.TextInput(
                       attrs={'class': 'form-group form-control', 'placeholder': 'e.g. John (Optional)'}),
                   'last_name': forms.TextInput(
                       attrs={'class': 'form-control form-group', 'placeholder': 'e.g. Doe (Optional)'})
                   }

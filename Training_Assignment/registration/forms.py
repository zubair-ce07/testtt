from django import forms
from django.contrib.auth.models import User
from django_countries.fields import LazyTypedChoiceField
from django.core.validators import RegexValidator
from django_countries import countries

from registration.models import UserProfile


class EditForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-group form-control'}))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-group form-control', 'placeholder': 'e.g. John (Optional)'}, ))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'e.g. Doe (Optional)', }, ))
    phone_number = forms.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")],
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'Format: +123456789 (Optional)'}))
    country = LazyTypedChoiceField(choices=countries, widget=forms.Select(attrs={'class': 'form-control form-group'}),
                                   required=False)
    address = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-group', 'placeholder': 'Address (Optional)'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control form-group'}))

    # def __init__(self, item_id):
    #     super(EditForm, self).__init__()
    #     self.fields['email'].queryset = User.objects.get(id=990).email
    #     print(self.fields.get('email'))


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$',
                       message="Phone number must be entered in the format: '+9999999999'.")],
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-control form-group', 'placeholder': 'Format: +123456789 (Optional)'}))

    # def save(self, commit=True):
    #     user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
    #                                     password=self.cleaned_data['password1'])
    #     user.save()
    #     self.user = user
    #     return super(CustomAccountForm, self).save(commit=commit)
    #
    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError("A user with that username already exists.")
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1", "")
    #     password2 = self.cleaned_data["password2"]
    #     if password1 != password2:
    #         raise forms.ValidationError("The two password fields didn't match.")
    #     return password2
    #
    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     try:
    #         User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return email
    #     raise forms.ValidationError("A user with that emailaddress already exists.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                            'placeholder': 'Email'}),
        }

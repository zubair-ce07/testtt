from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator, URLValidator


class SignupForm(forms.Form):
    error_css_class = 'error'
    first_name = forms.CharField(required=False, label='', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-bottom: 15px;', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=False, label='', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 15px;','placeholder': 'Last Name'}))
    email = forms.EmailField(required=False, label='', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control ', 'style':'margin-bottom: 15px;', 'placeholder': 'Email'}))
    username = forms.CharField(required=False, label='', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-bottom: 15px;', 'placeholder': 'User Name'}))
    password = forms.CharField(required=False, label='',max_length=100, widget=forms.TextInput
                                (attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password', 'style':'margin-bottom: 15px;'}))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        min_validator = MinLengthValidator(1)
        max_validator = MaxLengthValidator(50)
        try:
            min_validator(first_name)
        except:
            raise forms.ValidationError('First Name is required it couldn\'t be Blank')

        try:
            max_validator(first_name)
        except:
            raise forms.ValidationError('Length of First Name Shouldn\'t exceed 50')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        max_validator = MaxLengthValidator(50)
        try:
            max_validator(last_name)
        except:
            raise forms.ValidationError('Length of Last Name Shouldn\'t exceed 50')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except:
            raise forms.ValidationError('Email is not correct')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        min_validator = MinLengthValidator(1)
        max_validator = MaxLengthValidator(50)

        try:
            min_validator(username)
        except:
            raise forms.ValidationError('User Name is required it couldn\'t be Blank')

        try:
            max_validator(username)
        except:
            raise forms.ValidationError('Length of User Name Shouldn\'t exceed 50')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        min_validator = MinLengthValidator(8)
        max_validator = MaxLengthValidator(100)

        try:
            min_validator(password)
        except:
            raise forms.ValidationError('Minimum length required for password is 8')

        try:
            max_validator(password)
        except:
            raise forms.ValidationError('Length of Password Shouldn\'t exceed 100')

        return password


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


class AddMemoForm(forms.Form):
    title = forms.CharField(required=False, label='', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'style':'margin-bottom: 15px;'}))
    memo_text = forms.CharField(required=False, label='',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Memo Text', 'style':'margin-bottom: 15px;'}))
    url = forms.CharField(required=False, label='',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Url', 'style':'margin-bottom: 15px;'}))
    tags = forms.CharField(required=False, label='', max_length=300,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags, use comma seprated', 'style':'margin-bottom: 15px;'}))
    image = forms.FileField( label='Upload Image',
                            widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'image', 'placeholder': 'Upload Image','accept':'image/*',
                                                          'style':'margin-bottom: 15px;'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        min_validator = MinLengthValidator(1)
        max_validator = MaxLengthValidator(100)

        try:
            min_validator(title)
        except:
            raise forms.ValidationError('title cannot be empty')

        try:
            max_validator(title)
        except:
            raise forms.ValidationError('tilte is too long to valid')

        return title

    def clean_memo_text(self):
        memo_text = self.cleaned_data['memo_text']
        min_validator = MinLengthValidator(1)

        try:
            min_validator(memo_text)
        except:
            raise forms.ValidationError('Memo text cannot be empty')

        return memo_text

    def clean_url(self):
        url = self.cleaned_data['url']
        url_validator = URLValidator()

        try:
            url_validator(url)
        except:
            raise  forms.ValidationError('url is not valid')

        return url

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        min_validator = MinLengthValidator(1)
        max_validator = MaxLengthValidator(300)

        try:
            min_validator(tags)
        except:
            raise forms.ValidationError('Atleast one tag is required')

        try:
            max_validator(tags)
        except:
            raise forms.ValidationError('Tags are too long to valid')

        return tags

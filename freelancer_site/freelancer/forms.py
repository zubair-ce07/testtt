from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from freelancer.models import Employee, Project, Bids


class SignUpForm(UserCreationForm):
    CHOICES = [
        ('work', 'I want to work'),
        ('hire', 'I want to hire')
    ]
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Employee
        fields = ('user_type', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and self.instance.email != email and get_user_model().objects.filter(email=email).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UserProfileEditForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class PostProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields =('name', 'description', 'budget', )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7, 'cols': 25}),
        }


class UserBidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ("cover_letter", "bid_amount")
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 7, 'cols': 25}),
        }


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=[(x, x) for x in ['Select', 'Pending', 'Approve']],
                               widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))





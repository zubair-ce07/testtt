import datetime
from django import forms
from url_crawler.models import CustomUser


class UrlForm(forms.Form):
    """
    Form for input of url to crawl and collect meta data
    """
    url = forms.URLField(label='URL to crawl')


class LoginForm(forms.Form):
    """
    Form for providing login fields for user
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    """
    Form for creating a new user
    """
    date = datetime.datetime.now()
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, date.year+1)))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        """
        overriding default method and creating a user by setting password
        and date of birth from SelectDateWidget

        Arguments:
            commit (Boolean): save data to database ot not

        Returns:
            user (CustomUser): created user is returned
        """
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user

import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from taskmanager.models import Task, CustomUser
from taskmanager.validators import validate_user_profile_picture
from django.utils.safestring import mark_safe


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    due_date = forms.DateField(
        widget=forms.TextInput(attrs={
            "type": 'date',
            "min": datetime.date.today(),
            "value": datetime.date.today() + datetime.timedelta(days=7)
        })
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address',
                  'password1', 'password2']

    birthday = forms.DateField(

        widget=forms.TextInput(attrs={
            "type": 'date',
            "max": datetime.date.today()
        })
    )

    profile_picture = forms.ImageField(
        validators=[validate_user_profile_picture],
        help_text=mark_safe("<div> "
                            "<ul>"
                            "<li> Image should not be more than 500x500 pixels </li>"
                            "<li> Image should be of valid image type(jpeg, png, gif) </li>"
                            "<li> Image size not more than 20KB </li> "
                            "</div>")
    )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.address = self.cleaned_data["address"]
        user.birthday = self.cleaned_data["birthday"]
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'username', 'email', 'first_name', 'last_name', 'birthday', 'address', )

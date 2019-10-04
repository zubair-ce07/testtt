from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import FBUser


class FBUserCreationForm(UserCreationForm):

    class Meta:
        model = FBUser
        fields = ('username', 'email', 'profile_picture')


class FBUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = FBUser
        fields = ('email', 'profile_picture')
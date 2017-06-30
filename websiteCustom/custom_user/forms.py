from .models import CustomUser
from django import forms


class UserRegisterForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address1', 'address2', 'password']

    def save(self, commit=True):
        user_form = super(UserUpdateForm, self).save(commit=False)
        user = CustomUser.objects.get(id=user_form.pk)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        user.address1 = self.cleaned_data["address1"]
        user.address2 = self.cleaned_data["address2"]
        user.save()
        return user

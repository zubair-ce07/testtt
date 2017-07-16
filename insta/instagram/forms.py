from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.images import get_image_dimensions
from .models import User


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea)
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    # avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2', 'avatar', 'bio',)

    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user.set_password(user.password)
    #     if commit:
    #         user.save()
    #     return user

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    #
    # class Meta:
    #     model = User
    #     fields = ('email',)


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#
#     def clean_avatar(self):
#         avatar = self.cleaned_data['avatar']
#
#         try:
#             w, h = get_image_dimensions(avatar)
#
#             #validate dimensions
#             max_width = max_height = 100
#             if w > max_width or h > max_height:
#                 raise forms.ValidationError(
#                     u'Please use an image that is '
#                      '%s x %s pixels or smaller.' % (max_width, max_height))
#
#             #validate content type
#             main, sub = avatar.content_type.split('/')
#             if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
#                 raise forms.ValidationError(u'Please use a JPEG, '
#                     'GIF or PNG image.')
#
#             #validate file size
#             if len(avatar) > (20 * 1024):
#                 raise forms.ValidationError(
#                     u'Avatar file size may not exceed 20k.')
#
#         except AttributeError:
#             """
#             Handles case when we are updating the user profile
#             and do not supply a new avatar
#             """
#             pass
#
#         return avatar

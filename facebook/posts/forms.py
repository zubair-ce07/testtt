from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    description = forms.CharField()

    class Meta:
        model = Post
        fields = ('description', 'picture')
        exclude = ('fb_user', )
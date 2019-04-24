from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django import forms

from blogs.models import Blog


class BlogsForm(ModelForm):

    blog_date = forms.DateField( widget=forms.SelectDateWidget)

    class Meta:
        model = Blog
        fields = ['blog_text', 'blog_date' , 'status']

    def save(self,  request ,commit=True ):
        instance = super(BlogsForm, self).save(commit=False)
        instance.user_id = request.user.id
        instance.user_name = request.user.username
        if commit:
            instance.save()
        return instance
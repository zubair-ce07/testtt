from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django import forms

from blogs.models import Contents


class ArticleForm(ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1']


class TestForm(ModelForm):

    blog_date = forms.DateField( widget=forms.SelectDateWidget)


    #blog_text = forms.CharField(attrs={'size': 20000})

    class Meta:
        model = Contents
        fields = ['blog_text', 'blog_date' , 'status']

    def save(self,  request ,commit=True ):
        instance = super(TestForm, self).save(commit=False)
        instance.user_id = request.user.id
        instance.user_name = request.user.username
        if commit:
            instance.save()
        return instance
from datetime import datetime

from django import forms
from django.forms import DateTimeField

from blogs.models import Blog


class BlogForm(forms.ModelForm):
    published_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id': 'published_data', 'type': 'date'}), initial=datetime.now())

    #  DateTimeField(widget=forms.widgets.DateTimeInput(format="%d %b %Y %H:%M:%S %Z"))
    class Meta:
        model = Blog
        fields = ['id', 'blog_title', 'blog_description', 'published_date', 'user_id']

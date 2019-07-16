from django import forms

from .models import Article

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'authors', 'website', 'image_url', 'content', 'publish_time', 'url']
        
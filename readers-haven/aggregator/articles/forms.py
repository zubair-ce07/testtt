from django import forms

from articles.models import Article, Author, Website, Comment

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        
class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class NewWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = '__all__'

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

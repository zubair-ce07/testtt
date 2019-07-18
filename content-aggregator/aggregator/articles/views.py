from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.views import generic

from articles.models import Article, Author, Website
from articles.forms import NewArticleForm, NewAuthorForm, NewWebsiteForm

class IndexView(generic.ListView):
    template_name = 'articles/index.html'
    context_object_name = 'recent_articles'

    def get_queryset(self):
        return Article.objects.order_by('-publish_time')[:20]

class DetailView(generic.DetailView):
    model = Article
    template_name = 'articles/detail.html'

class ArticleForm(FormView):
    template_name = 'articles/add_article.html'
    form_class = NewArticleForm
    success_url = '/articles'

    def form_valid(self, form):
        print(form)
        article = Article.objects.create(
            title=form.cleaned_data['title'],
            category=form.cleaned_data['category'],
            website=form.cleaned_data['website'],
            image_url=form.cleaned_data['image_url'],
            content=form.cleaned_data['content'],
            publish_time=form.cleaned_data['publish_time'],
            url=form.cleaned_data['url'],
        )
        article.authors.add(*form.cleaned_data['authors'])
        return super(ArticleForm, self).form_valid(form)

class AuthorForm(FormView):
    template_name = 'articles/add_author.html'
    form_class = Author
    success_url = '/articles'

class WebsiteForm(FormView):
    template_name = 'articles/add_website.html'
    form_class = Website
    success_url = '/articles'

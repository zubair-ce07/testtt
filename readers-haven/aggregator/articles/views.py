from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.views import generic
from django.contrib import messages
from braces import views as braces_views

from articles.models import Article, Author, Website
from articles.forms import NewArticleForm, NewAuthorForm, NewWebsiteForm

class IndexView(generic.ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'recent_articles'
    paginate_by = 10
    queryset = Article.objects.order_by('-publish_time')

class DetailView(generic.DetailView):
    model = Article
    template_name = 'articles/detail.html'

class ArticleCreateView(braces_views.LoginRequiredMixin, braces_views.SuperuserRequiredMixin, FormView):
    template_name = 'articles/add_article.html'
    form_class = NewArticleForm
    success_url = '/'

    def form_valid(self, form):
        authors = form.cleaned_data.pop("authors")
        article = Article.objects.create(**form.cleaned_data)
        article.authors.add(*authors)
        return super(ArticleCreateView, self).form_valid(form)

class AuthorCreateView(braces_views.LoginRequiredMixin, braces_views.SuperuserRequiredMixin, FormView):
    template_name = 'articles/add_author.html'
    form_class = NewAuthorForm
    success_url = '/'

    def form_valid(self, form):
        Author.objects.create(**form.cleaned_data)
        return super(AuthorCreateView, self).form_valid(form)

class WebsiteCreateView(braces_views.LoginRequiredMixin, braces_views.SuperuserRequiredMixin, FormView):
    template_name = 'articles/add_website.html'
    form_class = NewWebsiteForm
    success_url = '/'

    def form_valid(self, form):
        Website.objects.create(**form.cleaned_data)
        return super(WebsiteCreateView, self).form_valid(form)

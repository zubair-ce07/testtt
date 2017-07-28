from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from news.models import News


class NewsView(LoginRequiredMixin, ListView):
    template_name = 'news/news.html'
    model = News
    context_object_name = 'all_news'


class NewsDetailedView(LoginRequiredMixin, DetailView):
    template_name = 'news/news_detail.html'
    model = News
    context_object_name = 'news'

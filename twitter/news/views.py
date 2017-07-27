from django.views.generic import ListView, DetailView

from news.models import News


class NewsView(ListView):
    template_name = 'news/news.html'
    model = News
    context_object_name = 'all_news'


class NewsDetailedView(DetailView):
    template_name = 'news/news_detailed.html'
    model = News
    context_object_name = 'news'

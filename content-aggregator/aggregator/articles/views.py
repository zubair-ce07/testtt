from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView

from .models import Article
from .forms import NewArticleForm

def index(request):
    recent_articles = Article.objects.order_by('-publish_time')[:10]
    return render(request, 'articles/index.html', {'recent_articles': recent_articles})

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'articles/detail.html', {'article': article})

class PostForm(FormView):
    template_name = 'articles/add_post.html'
    form_class = NewArticleForm
    success_url = '/articles'

# def add_post(request):
#     if request.method == 'POST':
#         form = NewArticleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_post')
#     else:
#         form = NewArticleForm()
#     return render(request, 'articles/add_post.html', {'form': form})

from django.shortcuts import render
from django.views import View
from .models import Post
from .forms import CreatePostForm


class PostView(View):
    @staticmethod
    def get(request):
        form = CreatePostForm()
        posts = Post.objects.all().order_by("id").reverse()
        return render(request, 'home.html', {'form': form, 'posts': posts})

    @staticmethod
    def post(request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.fb_user = request.user
            new_post.save()
            # resetting the from
            form = CreatePostForm()
            posts = Post.objects.all().order_by("id").reverse()
            return render(request, 'home.html', {'form': form, 'posts': posts})

from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Post


class AllPostsView(View):
    template_name = 'posts/all_posts.html'

    def get(self, request):
        posts = Post.objects.filter(is_expired=False)
        posts = posts.order_by('-id') if posts.exists() else []
        return render(request, self.template_name, dict(posts=posts))


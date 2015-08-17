from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Post


class MyPostsView(View):
    template_name = 'posts/my_posts.html'

    def get(self, request):
        posts = Post.objects.filter(Q(posted_by=request.user))
        posts = posts if posts.exists else None
        return render(request, self.template_name, dict(posts=posts))
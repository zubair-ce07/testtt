from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Post


class AllPostsView(View):
    template_name = 'posts/all_posts.html'

    def get(self, request):
        #TODO: Make sure to fetch only posts that are not yet expired.
        return render(request, self.template_name, dict(posts=Post.objects.all().order_by('-id')))


from django.shortcuts import render
from django.views.generic import View

from web.posts.models import Post


class HotPropertiesView(View):
    template_name = 'posts/all_posts.html'

    def get(self, request):
        return render(request, self.template_name,
                      dict(posts=sorted(Post.objects.all(), key=lambda m: -m.get_number_of_views)))

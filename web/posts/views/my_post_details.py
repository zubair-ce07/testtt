from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Post, Request, PostView


class MyPostDetailsView(View):

    template_name = 'posts/my_post_details.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        requests = Request.objects.filter(post=post)
        requests = requests if requests.exists() else []
        if not PostView.objects.filter(post_viewed=post, viewed_by=request.user).exists():
            PostView(viewed_by=request.user, post_viewed=post).save()
        return render(request, self.template_name, dict(requests=requests, post=post))
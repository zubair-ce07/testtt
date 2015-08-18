from django.db.models import Q

from django.shortcuts import render
from django.views.generic import View

from web.posts.models import Post, PostView, Request


class PostDetailsView(View):
    template_name = 'posts/post_details.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        requests = Request.objects.filter(post=post, requested_by=request.user)
        requests = requests if requests.exists() else []
        if not PostView.objects.filter(post_viewed=post, viewed_by=request.user).exists():
            PostView(viewed_by=request.user, post_viewed=post).save()
        is_owners_post = True if post.posted_by == request.user else False
        return render(request, self.template_name, dict(is_owners_post=is_owners_post, requests=requests, post=post))


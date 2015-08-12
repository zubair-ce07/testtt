from django.db.models import Q

from django.shortcuts import render
from django.views.generic import View

from web.posts.models import Post, PostView, Request


class PostDetailsView(View):
    template_name = 'posts/post_details.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        requests = Request.objects.filter(Q(post=post) & Q(requested_by=request.user))
        requests = requests if requests.exists() else None
        filter_criteria = Q(post_viewed=post) & Q(viewed_by=request.user)
        if not PostView.objects.filter(filter_criteria).exists():
            PostView(viewed_by=request.user, post_viewed=post).save()
        return render(request, self.template_name, dict(requests=requests, post=post))

    def post(self, request, post_id):
        response = None
        return response

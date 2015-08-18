from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Post, Request, PostView


class MyPostDetailsView(View):

    template_name = 'posts/my_post_details.html'

    def get(self, request, post_id):
        # TODO: No need to use Q object everywhere.
        post = Post.objects.get(Q(pk=post_id))
        requests = Request.objects.filter(Q(post=post))
        requests = requests if requests.exists() else []

        # TODO: use Q objects only when you want to create dynamic query. No need to use here.
        filter_criteria = Q(post_viewed=post) & Q(viewed_by=request.user)
        if not PostView.objects.filter(filter_criteria).exists():
            PostView(viewed_by=request.user, post_viewed=post).save()
        return render(request, self.template_name, dict(requests=requests, post=post))
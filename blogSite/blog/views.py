import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


class list_posts(ListView):

    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.all()
    template_name = 'blog/listDisplay.html'


class view_post(DetailView):

    model = models.Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(view_post, self).get_context_data(**kwargs)
        post = context['post']
        comment_body = models.Comment.objects.filter(post=post)
        comment_likes = [likes for _, likes in post.comment_likes().items()]
        comment = zip(comment_body, comment_likes)
        context['comments'] = comment
        context['like_post'] = post.post_likes()

        return context

    def post(self, request, **kwargs):
        vote_choice = {'up_vote': 1, 'down_vote': -1}
        post_id = kwargs.get('pk')

        if request.POST.get('vote'):
            vote = request.POST.get('vote')
            vote = vote_choice[vote]
            models.Like_post.objects.create(created_at=datetime.datetime.now(), post_id=post_id, user_id=1, vote=vote)

        else:
            vote = request.POST.get('commentvote')
            comment_id = request.POST.get('comment_id')
            vote = vote_choice[vote]
            models.Like_comment.objects.create(created_at=datetime.datetime.now(), comment_id=comment_id, user_id=1, vote=vote)

        return redirect('http://127.0.0.1:8000/blog/post/id/{}/'.format(post_id))

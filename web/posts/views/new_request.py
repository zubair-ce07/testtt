from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View

from web.posts.forms.new_request_form import NewRequestForm
from web.posts.models import Post, Request


class NewRequestView(View):
    template_name = 'posts/new_request.html'

    def get(self, request, post_id):
        return render(request, self.template_name, dict(post_id=post_id, new_request_form=NewRequestForm(
            initial={'requested_price': Post.objects.get(pk=post_id).demanded_price})))

    def post(self, request, post_id):
        new_request_form = NewRequestForm(request.POST)
        if new_request_form.is_valid():
            message = new_request_form.cleaned_data.get('message')
            requested_price = new_request_form.cleaned_data.get('requested_price')
            post = Post.objects.get(pk=post_id)
            Request(requested_by=request.user, post=post, message=message, price=requested_price).save()
            response = redirect(reverse('post_details', args=[post_id]))
        else:
            response = render(request, self.template_name, dict(new_request_form=new_request_form))
        return response

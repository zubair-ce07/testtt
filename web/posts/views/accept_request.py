from django.views.generic import View
from web.posts.models import Request
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class AcceptRequestView(View):

    def get(self, request, post_id, request_id):
        request = Request.objects.get(pk=request_id)
        request.status = 'accepted'
        request.save()
        return redirect(reverse('my_post_details', args=[post_id]))
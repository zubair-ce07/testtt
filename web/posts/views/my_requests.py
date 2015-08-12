from django.shortcuts import render
from django.views.generic import View
from web.posts.models import Request


class MyRequestsView(View):

    template_name = 'posts/my_requests.html'

    def get(self, request):
        requests = Request.objects.filter(requested_by=request.user)
        requests = requests if requests.exists() else None
        return render(request, self.template_name, dict(requests=requests))

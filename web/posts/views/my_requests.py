from django.shortcuts import render
from django.views.generic import View


class MyRequestsView(View):

    template_name = 'posts/my_requests.html'

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        pass

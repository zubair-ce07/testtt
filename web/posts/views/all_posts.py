from django.shortcuts import render
from django.views.generic import View


class AllPostsView(View):
    template_name = 'posts/all_posts.html'

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        pass

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class FileUploadView(View):
    template_name = 'posts/upload.html'

    def get(self, request):
        return render(request, self.template_name, dict())

    def post(self, request):
        return HttpResponse(content="success")


def my_post(request):
    if request.method == 'POST':
        return HttpResponse('hello world')
    elif request.method == 'GET':
        return render(request, 'posts/upload.html', dict())


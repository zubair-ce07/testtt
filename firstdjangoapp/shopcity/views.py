from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .controller import Controller


class FileUpload(View):
    template_name = "shopcity/uploadfile.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        status = Controller().handle_file(request.FILES['fileToUpload'])
        if status:
            return HttpResponse('Successfully inserted!!')
        else:
            return HttpResponse('Invalid File!!')

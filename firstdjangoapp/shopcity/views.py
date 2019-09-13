import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .controller import save_products


class FileUpload(View):
    template_name = "uploadfile.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        json_file = request.FILES['jsonfile']
        with open(json_file.temporary_file_path()) as json_file:
            try:
                raw_products = json.load(json_file)
            except ValueError:
                return HttpResponse('Invalid File!!')
            else:
                save_products(raw_products)
                return HttpResponse('Successfully inserted!!')

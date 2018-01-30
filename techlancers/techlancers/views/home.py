from django.views.generic import TemplateView
from django.shortcuts import render
from django.template import RequestContext



class Home(TemplateView):
    template_name = "home"

    def get(self, request):
        return render(request, 'index.html')

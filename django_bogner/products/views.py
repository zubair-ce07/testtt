from django.shortcuts import render
from django.views import generic
from .models import Category


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.all()

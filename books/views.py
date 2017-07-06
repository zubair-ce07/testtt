from django.shortcuts import render
from django.http import HttpResponse
from . import models


def search_form(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            books = models.Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_form.html', {'query': q, 'books': books})
        else:
            return render(request, 'books/search_form.html', {'query': q, 'error': True})
    else:
        return render(request, 'books/search_form.html')


def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_results.html', {'books': books, 'query': q})
    return render(request, 'books/search_form.html', {'error': error})

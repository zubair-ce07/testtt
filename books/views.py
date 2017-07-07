from django.shortcuts import render
from .models import Book


def search_form(request):
    books, query, error = None, None, None
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            books = Book.objects.filter(title__icontains=query)
        else:
            error = True
    return render(request, 'books/search_form.html', {'query': query, 'error': error, 'books': books})

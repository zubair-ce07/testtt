from django.shortcuts import render
from .models import Book


def search_form(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_form.html', {'query': query, 'books': books})
        else:
            return render(request, 'books/search_form.html', {'query': query, 'error': True})
    else:
        return render(request, 'books/search_form.html')

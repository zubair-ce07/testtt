from django.shortcuts import render
from books.models import Book


def search_form(request):
    if 'q' in request.GET:
        query = request.GET['q']
        context = {'query': query, 'error': True}
        if query:
            books = Book.objects.filter(title__icontains=query)
            context['books'] = books
            context['error'] = False
        return render(request, 'books/search_form.html', context)
    else:
        return render(request, 'books/search_form.html')

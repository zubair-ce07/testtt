"""Module for Books views."""
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Book, IssueBook, RequestBook


def home(request):
    """For viewing Book list."""
    context = {
        'posts': Book.objects.all()
    }
    return render(request, 'books/home.html', context)


class SearchResultsView(LoginRequiredMixin, ListView):
    """Class for Searching book title/author."""

    model = Book
    template_name = 'index.html'

    def get_queryset(self):
        """Get QuerySet method."""
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author_name__icontains=query)
        )
        if not object_list:
            messages.success(self.request, 'No search results found')
        else:
            return object_list


class BookCreateView(LoginRequiredMixin, CreateView):
    """Class for Book model creation."""

    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        """Check form validity method."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """Class for Book model update."""

    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        """Check form validity method."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """Class for Book model delete."""

    model = Book
    success_url = '/'


class BookDetailView(LoginRequiredMixin, DetailView):
    """Class for each book's detail view."""

    model = Book


class BooksListView(LoginRequiredMixin, ListView):
    """Class for Book's list view."""

    model = Book
    template_name = 'books/home.html'
    context_object_name = 'books'
    ordering = ['-title']


class IssueBookListView(ListView):
    """Class for Issuing book model list view."""

    model = IssueBook
    template_name = 'books/issuebook_detail.html'
    context_object_name = 'books'
    ordering = ['-user']


class UserRequestsListView(LoginRequiredMixin, ListView):
    """Class for Requesting book model list view."""

    model = RequestBook
    template_name = 'books/user_requests_detail.html'
    context_object_name = 'books'
    ordering = ['-user']


class IssuebookDeleteView(LoginRequiredMixin, View):
    """Class for returning book to library."""

    success_url = 'book-home'

    def get(self, request, pk):
        """Get method for book return."""
        return render(request, 'books/issuebook_confirm_delete.html')

    def post(self, request, pk):
        """Post method book return."""
        issue_book = IssueBook.objects.get(id=pk)
        issue_book.book.number_of_books += 1
        issue_book.book.save()
        issue_book.delete()
        return render(request, 'index.html')


class RequestbookDeleteView(LoginRequiredMixin, View):
    """Class-based View for deleting book request."""

    success_url = 'book-home'

    def get(self, request, pk):
        """Get method for removing book request."""
        return render(request, 'books/requestbook_confirm_delete.html')

    def post(self, request, pk):
        """Post method for removing book request."""
        request_book = RequestBook.objects.get(id=pk)
        request_book.delete()
        return redirect('direct_requests')


class MyIssuedBooks(LoginRequiredMixin, View):
    """View for viewing user's issued books."""

    success_url = '/'


class RequestView(LoginRequiredMixin, View):
    """Class for viewing user requests."""

    success_url = '/'


def BookRequest(request, pk):
    """For Requesting books."""
    book = get_object_or_404(Book, pk=pk)
    if IssueBook.objects.filter(user=request.user).count() == 3:
        messages.success(request, 'You have reached the max amount of books you can issue!')
        return redirect(request.META['HTTP_REFERER'])
    if RequestBook.objects.filter(user=request.user, title=book.title):
        messages.success(request, 'You have already submitted a request for this book!')
        return redirect(request.META['HTTP_REFERER'])
    if IssueBook.objects.filter(user=request.user, title=book.title):
        messages.success(request, 'You already have this book issued!')
        return redirect(request.META['HTTP_REFERER'])
    else:
        new_request_book = RequestBook(user=request.user, book=book, title=book.title,
                                       issue_date=datetime.now(), return_date=datetime.now() + timedelta(days=3))

        new_request_book.save()
        messages.success(request, 'New book request has been successfully submitted!')
        return redirect(request.META['HTTP_REFERER'])


def BookIssue(request, pk):
    """For Issuing books."""
    book = get_object_or_404(Book, pk=pk)
    requests = RequestBook.objects.filter(book=book)
    for each_request in requests:
        if IssueBook.objects.filter(user=each_request.user, title=book.title):
            messages.success(request, 'User has already issued this book!')
            return redirect(request.META['HTTP_REFERER'])
        elif IssueBook.objects.filter(user=each_request.user).count() == 3:
            messages.success(request, 'User has reached the maximum amount of books!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            new_book_issue = IssueBook(user=each_request.user, book=book, title=book.title,
                                       issue_date=datetime.now(), return_date=datetime.now() + timedelta(days=3))

            new_book_issue.save()
            book.number_of_books -= 1
            book.save()
            request_book = RequestBook.objects.filter(title=book.title, user=each_request.user)
            request_book.delete()
            return redirect(request.META['HTTP_REFERER'])


def user_profile(request, pk):
    """For viewing user information and user issued books."""
    user_request = RequestBook.objects.get(id=pk)
    issued_books = IssueBook.objects.filter(user=user_request.user)
    context = {'user': user_request.user,
               'issued_books': issued_books}
    return render_to_response('users/user_profile.html', context)

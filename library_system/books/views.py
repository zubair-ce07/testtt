"""Module for Books views."""
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from users.models import UserProfile
from users.constants import LIBRARIAN_GROUP_NAME
from .models import Book, IssueBook, RequestBook


class SearchBookView(LoginRequiredMixin, ListView):
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


class BookCreateView(LoginRequiredMixin, CreateView, UserPassesTestMixin,):
    """Class for Book model creation."""

    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        """Check form validity method."""
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """Check user validity."""
        is_librarian = UserProfile.objects.filter(
            id=self.request.user.id,
            groups__name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return True
        return False


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Class for Book update."""

    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        """Check form validity method."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class for Book model delete."""

    model = Book
    success_url = '/'

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name='LIBRARIAN_GROUP_NAME').exists()
        if is_librarian:
            return True
        return False


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
    context_object_name = 'issued_books'
    ordering = ['-user']


class UserRequestsListView(LoginRequiredMixin, ListView):
    """Class for Requesting book model list view."""

    model = RequestBook
    template_name = 'books/user_requests_detail.html'
    context_object_name = 'user_requests'
    ordering = ['-user']


class IssueBookDeleteView(LoginRequiredMixin, View):
    """Class for returning book to library."""

    success_url = 'book-home'

    def get(self, request, pk):
        """Get method for book return."""
        return render(request, 'books/issuebook_confirm_delete.html')

    def post(self, request, pk):
        """Post method book return."""
        try:
            issue_book = IssueBook.objects.get(id=pk)
            issue_book.book.number_of_books += 1
            issue_book.book.save()
            issue_book.delete()
            return render(request, 'index.html')
        except issue_book.DoesNotExist:
            messages.success(request, 'Issuebook model does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except issue_book.MultipleObjectsReturned:
            messages.success(request, 'More than one issuebook model was returned.')
            return redirect(request.META['HTTP_REFERER'])


class RequestbookDeleteView(LoginRequiredMixin, View):
    """Class-based View for deleting book request."""

    success_url = 'book-home'

    def get(self, request, pk):
        """Get method for removing book request."""
        return render(request, 'books/requestbook_confirm_delete.html')

    def post(self, request, pk):
        """Post method for removing book request."""
        try:
            request_book = RequestBook.objects.get(id=pk)
            request_book.delete()
            return redirect('direct_requests')
        except request_book.DoesNotExist:
            messages.success(request, 'Book request does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except request_book.MultipleObjectsReturned:
            messages.success(request, 'More than one book request was returned.')
            return redirect(request.META['HTTP_REFERER'])


class MyIssuedBooks(LoginRequiredMixin, View):
    """View for viewing user's issued books."""

    success_url = '/'

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return True
        return False


class UserRequestsView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Class for viewing user requests."""

    success_url = '/'


class UserProfileView(View):
    """For viewing user information and user issued books by librarian."""

    def get(self, request, pk):
        """Get method for requested book's user's profile."""
        try:
            user_request = RequestBook.objects.get(id=pk)
            issued_books = IssueBook.objects.filter(user=user_request.user)
            context = {'user': user_request.user,
                       'issued_books': issued_books}
            return render_to_response('users/user_profile.html', context)
        except user_request.DoesNotExist:
            messages.success(request, 'User request does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except user_request.MultipleObjectsReturned:
            messages.success(request, 'More than one user request was returned.')
            return redirect(request.META['HTTP_REFERER'])


class BookRequestView(View):
    """For Requesting books."""

    def get(self, request, pk):
        """Get method to request book."""
        try:
            book = Book.objects.get(id=pk)
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
                                               issue_date=datetime.now(),
                                               return_date=datetime.now() + timedelta(days=3))

                new_request_book.save()
                messages.success(request, 'New book request has been successfully submitted!')
                return redirect(request.META['HTTP_REFERER'])
        except book.DoesNotExist:
            messages.success(request, 'Book does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except book.MultipleObjectsReturned:
            messages.success(request, 'More than one book was returned.')
            return redirect(request.META['HTTP_REFERER'])


class BookIssueView(View):
    """For Issuing books."""

    def get(self, request, pk):
        """Get method to issue book."""
        try:
            book_request = RequestBook.objects.get(id=pk)
            book = book_request.book
            user = book_request.user
            if IssueBook.objects.filter(user=user).count() == 3:
                messages.success(request, 'User has reached the maximum amount of books!')
                return redirect(request.META['HTTP_REFERER'])
            if book.number_of_books == 0:
                messages.success(request, 'This book is not in stock anymore.')
                return redirect(request.META['HTTP_REFERER'])
            else:
                new_book_issue = IssueBook(user=user, book=book,
                                           title=book.title,
                                           issue_date=datetime.now(),
                                           return_date=datetime.now() + timedelta(days=3))

                new_book_issue.save()
                book.number_of_books -= 1
                book.save()
                request_book = RequestBook.objects.filter(title=book.title, user=user)
                request_book.delete()
                return redirect(request.META['HTTP_REFERER'])
        except book_request.DoesNotExist:
            messages.success(request, 'Book does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except book_request.MultipleObjectsReturned:
            messages.success(request, 'More than one book was returned.')
            return redirect(request.META['HTTP_REFERER'])

"""Module for Books views."""

import csv
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
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
            return is_librarian


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
            return is_librarian



class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class for Book model delete."""

    model = Book
    success_url = '/'

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name='LIBRARIAN_GROUP_NAME').exists()
        if is_librarian:
            return is_librarian


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

    @staticmethod
    def get(request, book_id):
        """Get method for book return."""
        return render(request, 'books/issuebook_confirm_delete.html')

    @staticmethod
    def post(request, book_id):
        """Post method book return."""
        try:
            issue_book = IssueBook.objects.get(id=book_id)
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

    @staticmethod
    def get(request, book_id):
        """Get method for removing book request."""
        return render(request, 'books/requestbook_confirm_delete.html')

    @staticmethod
    def post(request, book_id):
        """Post method for removing book request."""
        try:
            request_book = RequestBook.objects.get(id=book_id)
            request_book.delete()
            return redirect('direct_requests')
        except request_book.DoesNotExist:
            messages.success(request, 'Book request does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except request_book.MultipleObjectsReturned:
            messages.success(request, 'More than one book request was returned.')
            return redirect(request.META['HTTP_REFERER'])


class MyIssuedBooks(LoginRequiredMixin, ListView):
    """View for viewing user's issued books."""

    model = IssueBook
    template_name = 'books/issuebook_detail.html'
    context_object_name = 'issued_books'
    ordering = ['-book']

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return is_librarian


class UserRequestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Class for viewing user requests."""

    model = RequestBook
    template_name = 'books/user_requests_detail.html'
    context_object_name = 'user_requests'
    ordering = ['-book']

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return is_librarian


class UserProfileView(View):
    """For viewing user information and user issued books by librarian."""

    @staticmethod
    def get(request, book_id):
        """Get method for requested book's user's profile."""
        try:
            user_request = RequestBook.objects.get(id=book_id)
            issued_books = IssueBook.objects.filter(user=user_request.user)
            context = {'user': request.user,
                       'user_profile': user_request.user,
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

    @staticmethod
    def get(request, book_id):
        """Get method to request book."""
        try:
            book = Book.objects.get(id=book_id)
            if IssueBook.objects.filter(user=request.user).count() == 3:
                messages.success(request, 'You have reached the max amount of books you can issue!')
                return redirect(request.META['HTTP_REFERER'])
            if RequestBook.objects.filter(user=request.user, book=book):
                messages.success(request, 'You have already submitted a request for this book!')
                return redirect(request.META['HTTP_REFERER'])
            if IssueBook.objects.filter(user=request.user, book=book):
                messages.success(request, 'You already have this book issued!')
                return redirect(request.META['HTTP_REFERER'])

            new_request_book = RequestBook(user=request.user, book=book,
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

    @staticmethod
    def get(request, book_id):
        """Get method to issue book."""
        try:
            book_request = RequestBook.objects.get(id=book_id)
            book = book_request.book
            user = book_request.user
            if IssueBook.objects.filter(user=user).count() == 3:
                messages.success(request, 'User has reached the maximum amount of books!')
                return redirect(request.META['HTTP_REFERER'])
            if book.number_of_books == 0:
                messages.success(request, 'This book is not in stock anymore.')
                return redirect(request.META['HTTP_REFERER'])

            new_book_issue = IssueBook(user=user, book=book,
                                       issue_date=datetime.now(),
                                       return_date=datetime.now() + timedelta(days=3))

            new_book_issue.save()
            book.number_of_books -= 1
            book.save()
            request_book = RequestBook.objects.filter(book=book, user=user)
            request_book.delete()
            return redirect(request.META['HTTP_REFERER'])
        except book_request.DoesNotExist:
            messages.success(request, 'Book does not exist.')
            return redirect(request.META['HTTP_REFERER'])
        except book_request.MultipleObjectsReturned:
            messages.success(request, 'More than one book was returned.')
            return redirect(request.META['HTTP_REFERER'])


class BooksUpload(LoginRequiredMixin, UserPassesTestMixin, View):
    """Class for bulk creation of books from a csv file."""

    @staticmethod
    def get(request):
        """Get method for template rendering."""
        template = "books/book_upload.html"
        return render(request, template)

    @staticmethod
    def post(request):
        """Post method to read csv file and create books."""
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.success(request, "This is not a csv file.")
            next_url = request.POST.get('next', '/')
            return HttpResponseRedirect(next_url)

        file_data = csv_file.read().decode("UTF-8")
        csv_dicts_data = [{k: v for k, v in row.items()} for row in csv.DictReader(
            file_data.splitlines(), skipinitialspace=True)]
        for row in csv_dicts_data:
            Book.objects.update_or_create(
                title=row["title"],
                author_name=row["author_name"],
                publisher=row["publisher"],
                number_of_books=row["number_of_books"],
            )
        context = {'books': Book.objects.all()}
        return render(request, 'books/home.html', context)

    def test_func(self):
        """Check user validity."""
        is_librarian = self.request.user.groups.filter(
            name=LIBRARIAN_GROUP_NAME).exists()
        if is_librarian:
            return is_librarian

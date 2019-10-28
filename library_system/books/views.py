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
from users.models import UserProfile
from .models import Book, IssueBook, RequestBook




def home(request):
    context = {
        'posts': Book.objects.all()
    }
    return render(request, 'books/home.html', context)


class BooksListView(ListView):
    model = Book
    template_name = 'books/home.html' 
    context_object_name = 'books'
    ordering = ['-title']

class SearchResultsView(ListView):
    model = Book
    template_name = 'index.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author_name__icontains=query)
        )
        return object_list

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author_name', 'publisher', 'number_of_books']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BooksDetailView(DetailView):
    model = Book

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/'

class IssueBookListView(ListView):
    model = IssueBook
    template_name = 'books/issuebook_detail.html' 
    context_object_name = 'books'
    ordering = ['-user']

class UserListView(ListView):
    model = UserProfile
    template_name = 'books/user_detail.html' 
    context_object_name = 'users'
    ordering = ['-username']

class UserRequestsListView(ListView):
    model = RequestBook
    template_name = 'books/user_requests_detail.html' 
    context_object_name = 'books'
    ordering = ['-user']

class BorrowListView(ListView):
    model = IssueBook
    template_name = 'books/borrow_detail.html' 
    context_object_name = 'books'
    ordering = ['-user']

class IssuebookDeleteView(View):
    success_url = 'book-home'

    """Class-based View for Edit Profile Page."""
    def get(self, request,pk):
        """Get method for Edit Profile View."""
        return render(request, 'books/issuebook_confirm_delete.html')
    
    def post(self, request, pk):
        """Post method for Edit Profile View."""
        issue_book = IssueBook.objects.get(id=pk)
        issue_book.book.number_of_books +=1
        issue_book.book.save()
        self.request.user.book_count -=1
        self.request.user.save()
        issue_book.delete()     
        return render(request, 'index.html')

class RequestbookDeleteView(View):
    success_url = 'book-home'

    """Class-based View for Edit Profile Page."""
    def get(self, request,pk):
        """Get method for Edit Profile View."""
        return render(request, 'books/requestbook_confirm_delete.html')
    
    def post(self, request, pk):
        """Post method for Edit Profile View."""
        request_book = RequestBook.objects.get(id=pk)
        request_book.delete()    
        return redirect('direct_requests')

class MyView(View):
    success_url = '/'

class RequestView(View):
    success_url = '/'

def BookRequest(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if(request.user.book_count == 3):
        messages.success(request, 'You have reached the max amount of books you can issue!')
        return redirect(request.META['HTTP_REFERER'])
    if(RequestBook.objects.filter(user=request.user, title=book.title)):
        messages.success(request, 'You have already submitted a request for this book!')
        return redirect(request.META['HTTP_REFERER'])
    else:
        new_request_book = RequestBook(user=request.user, book=book, title=book.title,
                                        issue_date=datetime.now(), return_date=datetime.now() + timedelta(days=3))

        new_request_book.save()
        messages.success(request, 'New book request has been successfully submitted!')
        return redirect(request.META['HTTP_REFERER'])



def BookIssue(request, pk):
    book = get_object_or_404(Book, pk=pk)
    requests = RequestBook.objects.filter(book=book)
    for each_request in requests:
        if(IssueBook.objects.filter(user=each_request.user, title=book.title)):
            messages.success(request, 'User has already issued this book!')
            return redirect(request.META['HTTP_REFERER'])
        if(each_request.user.book_count == 3):
            messages.success(request, 'User has reached the maximum amount of books!')
            return redirect(request.META['HTTP_REFERER'])

        else:
            new_book_issue = IssueBook(user=each_request.user, book=book, title=book.title,
                                              issue_date=datetime.now(), return_date=datetime.now() + timedelta(days=3))

            new_book_issue.save()
            request.user.book_count +=1
            request.user.save()
            book.number_of_books -=1 
            book.save()
            request_book = RequestBook.objects.filter(title=book.title, user=each_request.user)
            request_book.delete()
            return redirect(request.META['HTTP_REFERER'])

def user_profile(request, pk):
    user_request = RequestBook.objects.get(id=pk)
    issued_books = IssueBook.objects.filter(user=user_request.user)
    context = {'user': user_request.user,
               'issued_books': issued_books}
    return render_to_response('books/user_profile.html', context)

def view_info(request, pk):
    user = UserProfile.objects.get(id=pk)
    issued_books = IssueBook.objects.filter(user=user)
    context = {'user': user,
               'issued_books': issued_books}
    return render_to_response('books/user_profile.html', context)

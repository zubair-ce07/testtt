# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from books.forms import BookForm, AuthorForm, PublisherForm
from books.models import Book, Author, Publisher


@login_required
def book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/books/books')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


@login_required
def author_form(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/books/authors')
    else:
        form = AuthorForm()
    return render(request, 'books/add_author.html', {'form': form})


@login_required
def publisher_form(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/books/publishers')
    else:
        form = PublisherForm()
    return render(request, 'books/add_publisher.html', {'form': form})


def index(request):
    books_list = Book.objects.order_by('-pub_date')
    authors_list = Author.objects.all()
    publisher_list = Publisher.objects.all()
    num_vist = request.session.get('visit_counter', 1)
    request.session['visit_counter'] = num_vist + 1
    context = {'books_list': books_list, 'authors_list': authors_list,
               'publisher_list': publisher_list, 'num_vist': num_vist}
    return render(request, 'books/index.html', context)


def books(request):
    books_list = Book.objects.all()
    context = {'books_list': books_list}
    return render(request, 'books/books.html', context)


def authors(request):
    authors_list = Author.objects.all()
    books_list = Book.objects.all()
    context = {'authors_list': authors_list, 'books_list': books_list}
    return render(request, 'books/authors.html', context)


def publishers(request):
    publisher_list = Publisher.objects.all()
    books_list = Book.objects.all()
    context = {'publisher_list': publisher_list, 'books_list': books_list}
    return render(request, 'books/publishers.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book}
    return render(request, 'books/book_details.html', context)


@method_decorator(csrf_exempt, name='dispatch')
def item_delete(request):
    if request.user.is_authenticated:
        item_id = request.POST['id']
        type_del = request.POST['type']
        try:
            if type_del == "book":
                Book.objects.filter(id=item_id).delete()
            elif type_del == "author":
                Author.objects.filter(id=item_id).delete()
            elif type_del == "publisher":
                Publisher.objects.filter(id=item_id).delete()
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponse("Cant find the record")
        return HttpResponse("done")
    else:
        return HttpResponse("Login Required to Delete any Item")


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books_list = Book.objects.filter(Q(authors__id=author_id))
    context = {'author': author, 'books_list': books_list}
    return render(request, 'books/author_details.html', context)


def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    books_list = Book.objects.filter(Q(publisher__id=publisher_id))
    context = {'publisher': publisher, 'books_list': books_list}
    return render(request, 'books/publisher_details.html', context)

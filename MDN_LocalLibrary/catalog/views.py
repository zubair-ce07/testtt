import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookModelForm


@login_required
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()

    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_genres': num_genres,
                           'num_visits': num_visits})


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status='o').order_by('due_back')


class LoanedBooksByAllListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('borrowed'))
    else:
        proposed_renewal_date = datetime.datetime.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')


class BookInstanceUpdateStatus(UpdateView):
    model = BookInstance
    fields = ['due_back', 'status', 'borrower', ]

    def get_success_url(self):
        if 'fk' in self.kwargs:
            return reverse('book-detail', kwargs={'pk': self.kwargs['fk']})
        return reverse('books')


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance

    def get_success_url(self):
        if 'fk' in self.kwargs:
            return reverse('book-detail', kwargs={'pk': self.kwargs['fk']})
        return reverse('books')


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance

    fields = '__all__'

    def get_initial(self):
        foreign_key = get_object_or_404(Book, pk=self.kwargs['fk'])
        return {'book': foreign_key}

    def get_success_url(self):
        if 'fk' in self.kwargs:
            return reverse('book-detail', kwargs={'pk': self.kwargs['fk']})
        return reverse('books')

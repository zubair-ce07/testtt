import json
import logging
import requests

from .constants import NoteAppConstants
from .models import NoteBook, Note
from datetime import datetime
from dateutil import parser as date_parser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.dispatch import Signal, receiver
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# Creating a custom signal to log a note creation message
note_book_created_signal = Signal(providing_args=['message'])

# Setting logging level to Debug. By default the logging level is set to Warning.
logging.basicConfig(filename='note_book.log', level=logging.DEBUG)


class PublicHomePageListView(generic.ListView):
    """ This view is displaying the all public note books and notes on home page """
    template_name = 'note/public/public_home.html'
    context_object_name = 'note_books'

    def get_context_data(self, **kwargs):
        context = super(PublicHomePageListView, self).get_context_data(**kwargs)
        context.update({
            'notes': Note.objects.filter(is_public=True).order_by(
                NoteAppConstants.NOTES_ORDER_BY_PUBLIC_PAGE)[:NoteAppConstants.NUMBER_OF_NOTES_PUBLIC_PAGE]
        })
        return context

    def get_queryset(self):
        return NoteBook.objects.filter(is_public=True).order_by(
            NoteAppConstants.NOTE_BOOKS_ORDER_BY_PUBLIC_PAGE)[:NoteAppConstants.NUMBER_OF_NOTE_BOOKS_PUBLIC_PAGE]


def search_by_keywords(request):
    """This method is returning note books and notes which matching the query
     Filtering data of logged In User by
     Note title
     Note description
     Note Book title
     """
    template_name = 'note/search_notes.html'
    query = request.GET.get('q')
    match_book_title = request.GET.get('match_book_title')
    if query is None:
        query = ''
    notes = Note.objects.filter(Q(title__icontains=query) |
                                Q(description__icontains=query)
                                ).filter(note_book__in=NoteBook.objects.filter(user=request.user))
    note_books = []
    if match_book_title == 'on':
        note_books = NoteBook.objects.filter(Q(title__icontains=query)).filter(user=request.user)

    context = {
        'notes': notes,
        'note_books': note_books
    }
    return render(request, template_name, context)


def search_books(request):
    """This method is returning note books by requesting the google books lib"""
    template_name = 'note/search_books.html'
    query = request.GET.get('q')
    context = {}

    if query:
        response = requests.get(NoteAppConstants.GOOGLE_BOOKS_API_URL+query)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            context = {'message': NoteAppConstants.SUCCESS, 'books': response_data['items']}
        elif response.status_code == 404:
            context = {'message': NoteAppConstants.NO_DATA_FOUND}
    return render(request, template_name, context)


class AllPublicNoteBookListView(generic.ListView):
    """Showing the list of all public note books"""
    template_name = 'note/public/public_note_books.html'
    context_object_name = 'note_books'
    paginate_by = NoteAppConstants.NUMBER_OF_NOTE_BOOKS_ALL_PAGE

    def get_queryset(self):
        return NoteBook.objects.filter(is_public=True).order_by(NoteAppConstants.NOTE_BOOKS_ORDER_BY_PUBLIC_PAGE)


class AllPublicNoteListView(generic.ListView):
    """Showing the list of all public notes"""
    template_name = 'note/public/public_notes.html'
    context_object_name = 'notes'
    paginate_by = NoteAppConstants.NUMBER_OF_NOTES_ALL_PAGE

    def get_queryset(self):
        return Note.objects.filter(is_public=True)


class HomePageListView(LoginRequiredMixin, generic.ListView):
    """Home page displayed after login containing the list of notes and note books created by logged in User"""
    template_name = 'note/home.html'
    context_object_name = 'note_books'
    paginate_by = NoteAppConstants.NUMBER_OF_NOTE_BOOKS_HOME_PAGE

    def get_queryset(self):
        return NoteBook.objects.filter(user=self.request.user).order_by(*NoteAppConstants.NOTE_BOOKS_ORDER_BY_HOME_PAGE)


class CreateNoteBook(LoginRequiredMixin, generic.CreateView):
    """Display the form for creating new note book"""
    model = NoteBook
    template_name = 'note/notebook_create.html'
    fields = ['title', 'author_name', 'publisher_name', 'published_date',
              'isbn', 'thumbnail', 'is_public', 'is_favorite']
    success_url = '/home'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, NoteAppConstants.NOTE_BOOK_CREATED)
        # Custom signal
        note_book_created_signal.send(NoteBook, message=NoteAppConstants.NOTE_BOOK_CREATED)
        return super().form_valid(form)


@receiver(note_book_created_signal)
def note_book_created_signal_receiver(sender, **kwargs):
    """Custom signal receiver for demonstration only"""
    logging.INFO(kwargs.get('message'))


class CreateNote(LoginRequiredMixin, generic.CreateView):
    """Display the form for creating new note"""
    model = Note
    template_name = 'note/note_create.html'
    fields = ['title', 'description', 'tags', 'thumbnail', 'is_public', 'is_favorite']

    def get_context_data(self, **kwargs):
        context = super(CreateNote, self).get_context_data(**kwargs)
        context.update({
            'note_book': get_object_or_404(NoteBook, pk=self.kwargs.get('note_book'))
        })
        return context

    def form_valid(self, form):
        form.instance.note_book = get_object_or_404(NoteBook, pk=self.kwargs.get('note_book'))
        messages.success(self.request, f'{NoteAppConstants.NOTE_CREATED}{form.instance.note_book.title}!')
        return super(CreateNote, self).form_valid(form)

    def get_success_url(self):
        return reverse('note-book-notes', kwargs={'pk': self.object.note_book_id})


class NoteListView(LoginRequiredMixin, generic.ListView):
    """Display the list of notes in a respective note book"""
    template_name = 'note/notes.html'
    model = Note
    context_object_name = 'notes'
    paginate_by = NoteAppConstants.NUMBER_OF_NOTE_LIST_NOTE_PAGE

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update({
            'note_book': get_object_or_404(NoteBook, pk=self.kwargs.get('pk'))
        })
        return context

    def get_queryset(self):
        return Note.objects.filter(note_book_id=self.kwargs.get('pk')).order_by(
            *NoteAppConstants.NOTES_ORDER_BY_NOTES_PAGE)


class DeleteNoteBook(LoginRequiredMixin, generic.DeleteView):
    """ Responsible for deleting the note book"""
    model = NoteBook
    success_url = '/home'


class UpdateNoteBook(LoginRequiredMixin, generic.UpdateView):
    """Display a form to update the note book"""
    model = NoteBook
    template_name = 'note/notebook_update.html'
    fields = ['title', 'author_name', 'publisher_name', 'published_date',
              'isbn', 'thumbnail', 'is_public', 'is_favorite']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, NoteAppConstants.NOTE_BOOK_UPDATE_MESSAGE)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('note-book-update', kwargs={'pk': self.object.pk})


class UpdateNote(LoginRequiredMixin, generic.UpdateView):
    """Display a form to update the note"""
    model = Note
    template_name = 'note/note_update.html'
    fields = ['title', 'description', 'tags', 'thumbnail', 'is_public', 'is_favorite']

    def form_valid(self, form):
        messages.success(self.request, NoteAppConstants.NOTE_UPDATE_MESSAGE)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('note-update', kwargs={'pk': self.object.pk})


class DeleteNote(LoginRequiredMixin, generic.DeleteView):
    """ Responsible for deleting the note"""
    model = Note
    success_url = '/home'


class AboutPageListView(generic.ListView):
    """ Display a fancy about page """
    template_name = 'note/about.html'

    def get_queryset(self):
        return []


class NotePublicView(generic.DetailView):
    """ Display a public note view """
    model = Note
    template_name = 'note/note_view.html'


class NotePublicListView(generic.ListView):
    """ Displays list of all public notes  """
    template_name = 'note/public/notes_public_view.html'
    model = Note
    context_object_name = 'notes'
    paginate_by = NoteAppConstants.NUMBER_OF_NOTE_LIST_PUBLIC_PAGE

    def get_context_data(self, **kwargs):
        context = super(NotePublicListView, self).get_context_data(**kwargs)
        context.update({
            'note_book': get_object_or_404(NoteBook, pk=self.kwargs.get('pk'))
        })
        return context

    def get_queryset(self):
        return Note.objects.filter(note_book_id=self.kwargs.get('pk'), is_public=True).order_by(
            NoteAppConstants.NOTES_ORDER_BY_PUBLIC_PAGE)


def add_google_lib_book(request):
    """Method responsible of adding new note book with details provide by google books library """
    if request.is_ajax():
        request_data = request.POST
        published_date = datetime.now()
        if request_data['published_date']:
            published_date = date_parser.parse(request_data['published_date'])

        note_book = NoteBook.objects.create(title=request_data['title'],
                                            author_name=request_data['authors'],
                                            publisher_name=request_data['publisher'],
                                            published_date=datetime.strftime(published_date, '%Y-%m-%d'),
                                            isbn=request_data['ISBN'],
                                            thumbnail_url=request_data['thumb'],
                                            user=request.user
                                            )
        note_book.save()
        messages.success(request, NoteAppConstants.NOTE_BOOK_CREATED)
        return HttpResponse(NoteAppConstants.NOTE_BOOK_CREATED)
    else:
        messages.success(request, NoteAppConstants.SOMETHING_WENT_WRONG)
        return HttpResponse(NoteAppConstants.SOMETHING_WENT_WRONG)

from django.urls import path, re_path
from .views import (
                    PublicHomePageListView,
                    HomePageListView,
                    AboutPageListView,
                    CreateNoteBook,
                    UpdateNoteBook,
                    DeleteNoteBook,
                    CreateNote,
                    NoteListView,
                    UpdateNote,
                    DeleteNote,
                    NotePublicView,
                    NotePublicListView,
                    AllPublicNoteBookListView,
                    AllPublicNoteListView,
                    search_by_keywords
)
from . import views

urlpatterns = [
    path('', PublicHomePageListView.as_view(), name='notes-public-page'),
    path('home/', HomePageListView.as_view(), name='notes-home-page'),
    path('about/', AboutPageListView.as_view(), name='notes-about-page'),
    path('note-book/create', CreateNoteBook.as_view(), name='note-book-create'),
    path('note-book/<int:pk>/update', UpdateNoteBook.as_view(), name='note-book-update'),
    path('note-book/<int:pk>/delete', DeleteNoteBook.as_view(), name='note-book-delete'),
    path('note/<int:note_book>/create', CreateNote.as_view(), name='note-create'),
    path('note-book/<int:pk>/notes', NoteListView.as_view(), name='note-book-notes'),
    path('note/<int:pk>/update', UpdateNote.as_view(), name='note-update'),
    path('notes/<int:pk>/view', NotePublicListView.as_view(), name='note-book-public-notes'),
    path('note/<int:pk>/delete', DeleteNote.as_view(), name='note-delete'),
    path('note/<int:pk>/view', NotePublicView.as_view(), name='note-public-view'),
    path('public-notes/', AllPublicNoteListView.as_view(), name='all-public-notes'),
    path('public-note-books/', AllPublicNoteBookListView.as_view(), name='all-public-note-books'),
    path('find/', search_by_keywords, name='find-notes'),
    re_path(r'^results/$', search_by_keywords, name='search-notes'),
]

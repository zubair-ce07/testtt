# pages/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Note
from .forms import NoteForm


def home(request):
    notes = Note.objects
    context = {'notes': notes}
    return render(request, 'home.html', context)


def add_note(request):
    if request.method == "POST":
        # Get the posted form
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note_form.save()
            return HttpResponseRedirect('/')
    else:
        note_form = NoteForm()
    return render(request, 'add_note.html', {'form': note_form})

# pages/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm


def home(request):
    notes = Note.objects.filter(user=request.user.username)
    context = {'notes': notes}
    return render(request, 'home.html', context)


def add_note(request):
    if request.method == "POST":
        # Get the posted form
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            filled_form = note_form.save(commit=False)
            filled_form.user = request.user.username
            filled_form.save()
            return HttpResponseRedirect('/')
    else:
        note_form = NoteForm()
    return render(request, 'add_note.html', {'form': note_form})


def delete_note(request, note_id):
    Note.objects.get(id=note_id).delete()
    return redirect('/')

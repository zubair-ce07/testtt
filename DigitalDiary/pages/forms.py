from django import forms
from .models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'body', 'date')
        widgets = {
            'body': forms.Textarea,
            'date': forms.SelectDateWidget(),
        }

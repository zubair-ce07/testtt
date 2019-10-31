from django import forms
from .models import NoteBook


class NoteBookCreationForm(forms.ModelForm):
    class Meta:
        model = NoteBook
        fields = '__all__'

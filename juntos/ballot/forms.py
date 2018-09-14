from django import forms
from .models import Question, Choice, Tag


class AskForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label='Question')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Question
        fields = ['title']
        help_texts = {'tags': "Unique identifier for the student",}

    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['tags'] = kwargs['instance'].tags.all()

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'tags' field
    def save(self, commit=True):
        question = super().save()
        question.tags.set(self.cleaned_data['tags'])
        question.save()
        return question


class ChoiceForm(forms.ModelForm):
    text = forms.CharField(
        max_length=255, label="Choice")

    class Meta:
        model = Choice
        exclude = ('question',)
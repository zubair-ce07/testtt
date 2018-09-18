from django import forms
from .models import Ballot, Tag


class BallotForm(forms.ModelForm):
    """
    Ballot model form
    """
    title = forms.CharField(max_length=255, label='Ballot Title')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), help_text='Press ctrl and select more than one.')

    class Meta:
        model = Ballot
        fields = ['title', 'active_period']
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

    def save(self, commit=True):
        """Overriding save allows us to process the value of 'tags' field"""
        ballot = super().save()
        ballot.tags.set(self.cleaned_data['tags'])
        ballot.save()
        return ballot

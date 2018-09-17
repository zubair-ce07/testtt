from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.forms import modelformset_factory

from .decorators import admin_only
from .models import Ballot, Choice, Vote
from .forms import BallotForm


class BallotView(View):

    ChoiceFormFactory = modelformset_factory(Choice, fields=('text',), min_num=3, extra=0)

    @admin_only
    def get(self, request, id=None):
        new_ballot = False

        if id:
            ballot = get_object_or_404(Ballot, id=id)
            ballot_form = BallotForm(instance=ballot)
            choices = ballot.choice_set.all()
            choice_forms = self.ChoiceFormFactory(queryset=choices)
            template = 'ballot/ballot_form.html'
        else:
            ballot_form = BallotForm(instance=None)
            choice_forms = self.ChoiceFormFactory(queryset=Choice.objects.none())
            template = 'ballot/ballot_form.html'
            new_ballot = True

        context = {
            'ballot_form': ballot_form,
            'choice_forms': choice_forms,
            'new_ballot': new_ballot
        }

        return render(request, template, context)

    @admin_only
    def post(self, request, id=None):
        ballot = None
        if id:  # Means already existing Ballot is being edited.
            ballot = get_object_or_404(Ballot, id=id)
        ballot_form = BallotForm(request.POST, instance=ballot)
        choice_forms = self.ChoiceFormFactory(request.POST)

        if ballot_form.is_valid() and choice_forms.is_valid():
            new_ballot = ballot_form.save(commit=False)
            new_ballot.created_by = request.user
            new_ballot.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.ballot = new_ballot
                new_choice.save()
            return HttpResponseRedirect(reverse('ballot:ballot_list'))

        context = {'ballot_form': ballot_form, 'choice_forms': choice_forms}
        return render(request, 'ballot/ballot_form.html', context)


class BallotDeleteView(DeleteView):
    model = Ballot
    success_url = reverse_lazy('ballot:ballot_list')


class BallotListView(generic.ListView):
    """
    Index detailed view to show user information
    """
    model = Ballot
    template_name = 'ballot/index.html'
    context_object_name = 'ballots'

    def get_queryset(self):
        return (Ballot.objects
                .filter(is_active=True)
                .order_by('-created_at'))


class BallotDetailView(generic.DetailView):
    """
    Ballot detailed view to show user information
    """
    model = Ballot
    template_name = 'ballot/details.html'
    context_object_name = 'ballot'


def vote_ballot(request, id=None):
    context = {}
    ballot = get_object_or_404(Ballot, id=id)
    context["ballot"] = ballot

    if request.user.vote_set.filter(choice__ballot_id=ballot.id):
        context["error"] = "You've already voted for this ballot."
        return render(request, 'ballot/ballot.html', context)

    if request.method == "POST":
        Vote.objects.create(user=request.user, choice_id=request.POST['choice'])
        return HttpResponseRedirect(reverse('ballot:ballot_details', args=[ballot.id]))
    else:
        return render(request, 'ballot/ballot.html', context)

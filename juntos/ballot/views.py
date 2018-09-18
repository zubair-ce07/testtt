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
    """
    Ballot view manages both get and post for adding/editing balloting.
    """

    ChoiceFormFactory = modelformset_factory(Choice, fields=('text',), min_num=3, extra=0)

    @admin_only
    def get(self, request, id=None):
        """
        Get method during showing new ballot form/edit ballot form
        :param request: Request
        :param id: pk for ballot during editing
        :return: Render ballot_form.html with form context
        """
        new_ballot = False
        template = 'ballot/ballot_form.html'

        if id:
            # If editing existing Ballot
            ballot = get_object_or_404(Ballot, id=id)
            ballot_form = BallotForm(instance=ballot)
            choices = ballot.choice_set.all()
            choice_forms = self.ChoiceFormFactory(queryset=choices)

        else:
            # If new ballot is to be added.
            ballot_form = BallotForm(instance=None)
            choice_forms = self.ChoiceFormFactory(queryset=Choice.objects.none())
            new_ballot = True

        context = {
            'ballot_form': ballot_form,
            'choice_forms': choice_forms,
            'new_ballot': new_ballot
        }

        return render(request, template, context)

    @admin_only
    def post(self, request, id=None):
        """
        Saving ballot form
        :param request: Request
        :param id: If editing a ballot
        :return: Rendering to ballot listing or back to form view in case of errors.
        """
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
    """
    Ballot delete view.
    """
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
        """
        Provide all active ballots
        :return: Active ballots
        """
        return Ballot.objects.get_active_ballots()


class BallotDetailView(generic.DetailView):
    """
    Ballot detailed view to show user information
    """
    model = Ballot
    template_name = 'ballot/details.html'
    context_object_name = 'ballot'


def vote_ballot(request, id=None):
    """
    Vote ballot view manages both get and post requests, and ensure that user don't vote more than once.
    :param request: Request
    :param id: Id of ballot
    :return: Render to ballot_details in vote successfully else to ballot.html with ballot.
    """
    context = {}
    ballot = get_object_or_404(Ballot, id=id)
    context["ballot"] = ballot
    already_voted = request.user.vote_set.filter(choice__ballot_id=ballot.id)
    if already_voted:
        context["error"] = "You've already voted for this ballot."

    if request.method == "POST" and not already_voted:
        Vote.objects.create(user=request.user, choice_id=request.POST['choice'])
        return HttpResponseRedirect(reverse('ballot:ballot_details', args=[ballot.id]))
    else:
        return render(request, 'ballot/ballot.html', context)

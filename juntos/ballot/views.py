from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic import View

from .decorators import admin_hr_required
from .models import Question, Choice, Answer
from .forms import AskForm, ChoiceForm


class BallotView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            ballot_form = AskForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'ballot/edit_ballot.html'
        else:
            ballot_form = AskForm(instance=None)
            choice_forms = [
                ChoiceForm(prefix=str(x), instance=Choice())
                for x in range(3)
            ]
            template = 'ballot/new_ballot.html'
        context = {'ballot_form': ballot_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    def post(self, request, id=None):
        if id:  # Means already existing question is being edited.
            return self.put(request, id)
        ballot_form = AskForm(request.POST, instance=None)
        choice_forms = [
            ChoiceForm(request.POST, prefix=str(x), instance=Choice())
            for x in range(0, 3)
        ]
        if ballot_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_ballot = ballot_form.save(commit=False)
            new_ballot.created_by = request.user
            new_ballot.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_ballot
                new_choice.save()
            return HttpResponseRedirect(reverse('ballot:ballot_list'))
        context = {'ballot_form': ballot_form, 'choice_forms': choice_forms}
        return render(request, 'ballot/new_ballot.html', context)

    def put(self, request, id=None):
        question = get_object_or_404(Question, id=id)
        ballot_form = AskForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if ballot_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_ballot = ballot_form.save(commit=False)
            new_ballot.created_by = request.user
            new_ballot.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_ballot
                new_choice.save()
            return redirect('ballot:ballot_list')
        context = {'ballot_form': ballot_form, 'choice_forms': choice_forms}
        return render(request, 'ballot/edit_ballot.html', context)


class BallotDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('ballot:ballot_list')


class BallotListView(generic.ListView):
    """
    Index detailed view to show user information
    """
    model = Question
    template_name = 'ballot/index.html'
    context_object_name = 'questions'


class BallotDetailView(generic.DetailView):
    """
    Ballot detailed view to show user information
    """
    model = Question
    template_name = 'ballot/details.html'
    context_object_name = 'question'


def vote_ballot(request, id=None):
    context = {}
    question = get_object_or_404(Question, id=id)
    context["question"] = question

    if request.method == "POST":
        vote = Answer.objects.create(user=request.user, choice_id=request.POST['choice'])
        if vote:
            return HttpResponseRedirect(reverse('ballot:ballot_details', args=[question.id]))
        else:
            context["error"] = "Your vote is not done successfully"
            return render(request, 'ballot/ballot.html', context)
    else:
        return render(request, 'ballot/ballot.html', context)

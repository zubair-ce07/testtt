# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Trainee, Trainer, Technology, Assignment
from forms import LoginForm
from django.contrib.auth.models import User


def training_index(request):
    trainers_list = Trainer.objects.all()
    template = loader.get_template('training/training_index.html')
    context = {
        'trainers_list': trainers_list,
    }
    return HttpResponse(template.render(context, request))


def trainee_details(request, trainee_id):
    trainee = Trainee.objects.get(id=trainee_id)
    template = loader.get_template('training/trainee_details.html')
    context = {
        'trainee': trainee,
        'assignments': trainee.assignments.filter()
    }
    return HttpResponse(template.render(context, request))


def trainer_details(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    template = loader.get_template('training/trainer_details.html')
    context = {
        'trainer': trainer,
        'assignments': trainer.assignments.filter(),
        'trainee': trainer.trainee
    }
    return HttpResponse(template.render(context, request))


def assignment_details(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    template = loader.get_template('training/assignment_details.html')
    context = {
        'assignment': assignment
    }
    return HttpResponse(template.render(context, request))


def technology_details(request, technology_id):
    technology = Technology.objects.get(id=technology_id)
    template = loader.get_template('training/technology_details.html')
    context = {
        'technology': technology
    }
    return HttpResponse(template.render(context, request))


def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            trainees = Trainee.objects.filter(name=q)
            return render(request, 'training/trainee_search_results.html',
                                   {'trainees': trainees, 'query': q})
    return render(request, 'training/search_trainees.html',
                           {'error': error})


def login(request):
    form = LoginForm(request.POST)
    message = ''
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(self.request, user)
            # Redirect to a success page.
            return render(request, 'training/training_index.html')
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data

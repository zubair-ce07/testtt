# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Trainee, Trainer, Technology, Assignment


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
        'trainees': trainer.trainees.filter()
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
        'technology': technology,
        'assignments': trainer.assignments.filter(),
        'trainees': trainer.trainees.filter()
    }
    return HttpResponse(template.render(context, request))

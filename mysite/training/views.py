# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Trainee, Trainer, Technology, Assignment
from forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def training_index(request):
    trainers_list = Trainer.objects.all()
    template = loader.get_template('training/training_index.html')
    name = ""
    if request.user.first_name:
        name = request.user.first_name
    else:
        name = request.user.username

    context = {
        'user_name': name,
        'trainers_list': trainers_list,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def trainee_details(request, trainee_id):
    trainee = Trainee.objects.get(id=trainee_id)
    template = loader.get_template('training/trainee_details.html')

    context = {
        'trainee': trainee,
        'assignments': trainee.assignments.all(),
        'image_url': trainee.picture.url
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def trainer_details(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    template = loader.get_template('training/trainer_details.html')

    context = {
        'trainer': trainer,
        'assignments': trainer.assignments.all(),
        'trainee': trainer.trainee,
        'image_url': trainer.picture.url
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def assignment_details(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    template = loader.get_template('training/assignment_details.html')
    context = {
        'assignment': assignment
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def technology_details(request, technology_id):
    technology = Technology.objects.get(id=technology_id)
    template = loader.get_template('training/technology_details.html')
    context = {
        'technology': technology
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            trainees = Trainee.objects.filter(name__contains=q)
            return render(request, 'training/trainee_search_results.html',
                                   {'trainees': trainees, 'query': q})
    return render(request, 'training/search_trainees.html',
                           {'error': error})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('training_index'))

    template_name = 'training/login.html'
    if not request.POST:
        form = LoginForm(None)
        return render(request, template_name, {'form': form})

    form = LoginForm(request.POST)
    message = ''
    username = ''
    password = ''
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
    else:
        message = "Enter username and password"
    user = authenticate(username=username, password=password)

    if user and user.is_active:
        django_login(request, user)
        # Redirect to a success page.
        return redirect(reverse(training_index))
    else:
        message = "login failed"
    return render(request, template_name, {'error': message,
                                           'form': form})


def signup(request):
    template_name = 'training/signup.html'
    if request.user.is_authenticated:
        return redirect(reverse('training_index'))
    if not request.POST:
        form = SignUpForm(None)
        return render(request, template_name, {'form': form})
    form = SignUpForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect(reverse('login'))
    return render(request, template_name, {'form': form})


def logout(request):
    django_logout(request)
    return redirect(reverse('login'))

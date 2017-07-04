# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import (
    authenticate, login as django_login,
    logout as django_logout
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import View

from .models import Trainee, Trainer, Technology, Assignment
from .forms import LoginForm, SignUpForm, ProfileForm


class TrainingIndex(LoginRequiredMixin, View):
    template_name = 'training/training_index.html'
    login_url = 'training:login'
    name = ''

    def get(self, request):
        trainees_list = Trainee.objects.all()

        if request.user.first_name:
            self.name = request.user.first_name
        else:
            self.name = request.user.username

        context = {
            'user_name': self.name,
            'trainees_list': trainees_list,
        }
        return render(request, self.template_name, context)


class TraineeDetails(LoginRequiredMixin, View):
    template_name = 'training/trainee_details.html'
    login_url = 'training:login'

    def get(self, request, trainee_id):
        try:
            trainee = Trainee.objects.get(id=trainee_id)
        except Traineeself.DoesNotExist:
            raise Http404("Trainee does not exist")

        context = {
            'trainee': trainee,
            'assignments': trainee.assignments.all(),
            'image_url': trainee.user.user_profile.picture.url
        }
        return render(request, self.template_name, context)


class TrainerDetails(LoginRequiredMixin, View):
    template_name = 'training/trainer_details.html'
    login_url = 'training:login'

    def get(self, request, trainer_id):

        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            raise Http404("Trainer does not exist")

        context = {
            'trainer': trainer,
            'trainees': trainer.trainees.all(),
            'image_url': trainer.user.user_profile.picture.url
        }
        return render(request, self.template_name, context)


class AssignmentDetails(LoginRequiredMixin, View):
    template_name = 'training/assignment_details.html'
    login_url = 'training:login'

    def get(self, request, assignment_id):
        assignment = Assignment.objects.get(id=assignment_id)
        context = {
            'assignment': assignment
        }
        return render(request, self.template_name, context)


class TechnologyDetails(LoginRequiredMixin, View):
    template_name = 'training/technology_details.html'
    login_url = 'training:login'

    def get(self, request, technology_id):
        technology = Technology.objects.get(id=technology_id)
        context = {
            'technology': technology
        }
        return render(request, self.template_name, context)


class Search(LoginRequiredMixin, View):
    template_name = 'training/trainee_search_results.html'
    login_url = 'training:login'

    def get(self, request):
        error = False
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                error = True
            else:
                trainees = Trainee.objects.filter(name__contains=q)
                context = {
                    'trainees': trainees, 'query': q
                }
                return render(request, self.template_name, context)
        context = {
            'error': error
        }
        return render(request, 'training/search_trainees.html', context)


class Login(View):
    template_name = 'training/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('training:training_index'))
        form = LoginForm(None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)
        messages = []
        username = ''
        password = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user and user.is_active:
                django_login(request, user)
                '''Redirect to a success page.'''
                return redirect("training:training_index")
            else:
                messages.append("login failed")

        else:
            messages.append("Enter username and password")

        context = {
            'errors': messages,
            'form': form
        }
        return render(request, self.template_name, context)


class Signup(View):
    template_name = 'training/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('training:training_index')

        return render(request, self.template_name)


class TrainerSignUp(View):
    template_name = 'training/trainer_signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('training:training_index'))

        user_form = SignUpForm(None)
        # profile_form = ProfileForm(None)
        context = {
            'user_form': user_form,
            # 'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # profile_form = ProfileForm(request.POST)
        user_form = SignUpForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)

            # profile.picture = profile_form.cleaned_data['picture']

            # import pdb; pdb.set_trace()

            # profile.save()

            user.save()
            return redirect(reverse('training:login'))

        context = {
            'user_form': user_form,
            # 'profile_form': profile_form
        }
        return render(request, self.template_name, context)


class Logout(View):

    def get(self, request):
        django_logout(request)
        return redirect('training:login')

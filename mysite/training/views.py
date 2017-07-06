# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import (
    authenticate, login as django_login,
    logout as django_logout
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Trainee, Trainer, Technology, Assignment, UserProfile
from .forms import LoginForm, SignUpForm


class TrainingIndex(LoginRequiredMixin, View):
    template_name = 'training/training_index.html'
    login_url = 'training:login'
    name = ''

    def get(self, request):
        trainers = Trainer.objects.all()
        try:
            request.user.trainer
            status = "Trainer"
        except Exception as e:
            status = "Trainee"

        context = {
            'status': status,
            'trainers': trainers,
        }
        return render(request, self.template_name, context)


class TraineeDetails(LoginRequiredMixin, View):
    template_name = 'training/trainee_details.html'
    login_url = 'training:login'

    def get(self, request, trainee_id):
        try:
            trainee = Trainee.objects.get(id=trainee_id)
        except Trainee.DoesNotExist:
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
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            raise Http404("Assignment does not exist")

        context = {
            'assignment': assignment
        }
        return render(request, self.template_name, context)


class TechnologyDetails(LoginRequiredMixin, View):
    template_name = 'training/technology_details.html'
    login_url = 'training:login'

    def get(self, request, technology_id):
        try:
            technology = Technology.objects.get(id=technology_id)
        except Technology.DoesNotExist:
            raise Http404("Technology does not exist")

        context = {
            'technology': technology
        }
        return render(request, self.template_name, context)


class Search(LoginRequiredMixin, View):
    template_name = 'training/search_results.html'
    login_url = 'training:login'

    def get(self, request):
        error = False
        if 'q' in request.GET:
            q = request.GET.get('q')
            if not q:
                error = True
            else:
                try:
                    users = UserProfile.objects.filter(name__contains=q)

                except Trainee.DoesNotExist:
                    raise Http404("Trainee does not exist")

                context = {
                    'users': users, 'query': q
                }
                return render(request, self.template_name, context)
        context = {
            'error': error
        }
        return render(request, 'training/search_users.html', context)


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
    template_name = 'training/user_signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('training:training_index'))

        user_form = SignUpForm(None)
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = SignUpForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if not user:
                user_form.save_trainer()
                return redirect(reverse('training:login'))
            else:
                error = "User name already exists"
        else:
            error = "Fill all fields"

        context = {
            'user_form': user_form,
            'error': error
        }
        return render(request, self.template_name, context)


class TraineeSignUp(View):
    template_name = 'training/user_signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('training:training_index'))

        user_form = SignUpForm(None)
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = SignUpForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if not user:
                user_form.save_trainee()
                return redirect(reverse('training:login'))
            else:
                error = "User name already exists"
        else:
            error = "Fill all fields"

        context = {
            'user_form': user_form,
            'error': error
        }
        return render(request, self.template_name, context)


class Logout(View):

    def get(self, request):
        django_logout(request)
        return redirect('training:login')

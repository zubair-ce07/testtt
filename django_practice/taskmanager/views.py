from __future__ import absolute_import

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from taskmanager.forms import TaskForm, UserRegistrationForm, UpdateProfileForm
from taskmanager.models import Task, CustomUser


class TaskIndexView(ListView):
    template_name = 'task_index.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all().order_by('due_date')
        context = {
            'tasks': tasks,
        }
        return render(request, self.template_name, context)


class TaskDetailView(DetailView):
    template_name = 'task_detail.html'

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        context = {
            'task': task
        }
        return render(request, self.template_name, context)


class CreateTaskView(LoginRequiredMixin, CreateView):
    template_name = 'create_task.html'

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created, an email will be sent to you soon!')
        return redirect('task_index')


class EditTaskView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_task.html'

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        form = TaskForm(instance=task)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if request.user.username == form.cleaned_data['assignee'].username \
                    or request.user.username == form.cleaned_data['assigned_by'].username:
                form.save()
                messages.success(request, 'Task updated!')
                return redirect('task_index')
            messages.error(request, 'Not authorized')
            return redirect('task_index')
        return render(request, self.template_name, {'task': task})


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    template_name = "delete_task.html"

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        return render(request, self.template_name, {'task': task})

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_index')


class UserDetailView(DetailView):
    template_name = 'user_detail.html'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        context = {
            'user': user
        }
        return render(request, self.template_name, context)


class EditUserView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_user.html'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        form = UpdateProfileForm(instance=user)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user.id)
        return render(request, self.template_name, {'user': user})


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/password_change_form.html'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        form = PasswordChangeForm(user=user)
        return render(request, self.template_name, {
            'form': form,
            'user': user
        })

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        form = PasswordChangeForm(request.POST, instance=user)
        if form.is_valid():
            saved_form = form.save()
            update_session_auth_hash(request, saved_form)
            return redirect('user_detail', user.id)
        return render(request, self.template_name, {'user': user})


def redirect_task_index(request):
    return redirect('task_index')


class Register(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                raise ValueError('user was not authenticated')
            return redirect('task_index')
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

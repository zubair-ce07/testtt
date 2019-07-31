from __future__ import absolute_import
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from taskmanager.forms import TaskForm, UserRegistrationForm, UpdateProfileForm
from taskmanager.models import Task, CustomUser


def task_index(request):
    tasks = Task.objects.all().order_by('due_date')
    context = {
        'tasks': tasks,
    }
    return render(request, 'task_index.html', context)


def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    context = {
        'task': task
    }
    return render(request, 'task_detail.html', context)


def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        raise Http404
    context = {
        'user': user
    }
    return render(request, 'user_detail.html', context)


@login_required
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created, an email will be sent to you soon!')
        return redirect('task_index')

    context = {
        'form': form
    }
    return render(request, 'create_task.html', context)


@login_required
def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if request.user.username == form.cleaned_data['assignee'].username \
                    or request.user == form.cleaned_data['assigned_by'].username:
                form.save()
                messages.success(request, 'Task updated!')
                return redirect('task_index')
            messages.error(request, 'Not authorized')
            return redirect('task_index')
        return render(request, 'edit_task.html', {'task': task})
    context = {
        'form': form
    }
    return render(request, 'edit_task.html', context)


@login_required
def edit_user(request, pk):
    user = CustomUser.objects.get(id=pk)
    form = UpdateProfileForm(instance=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user.id)
        return render(request, 'edit_user.html', {'user': user})
    context = {
        'form': form
    }
    return render(request, 'edit_user.html', context)


@login_required
def change_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    form = PasswordChangeForm(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, instance=user)
        if form.is_valid():
            saved_form = form.save()
            update_session_auth_hash(request, saved_form)
            return redirect('user_detail', user.id)
        return render(request, 'registration/password_change_form.html', {'user': user})
    return render(request, 'registration/password_change_form.html', {
        'form': form,
        'user': user
    })


@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_index')
    return render(request, 'delete_task.html', {'task': task})


def redirect_task_index(request):
    return redirect('task_index')


def register(request):
    if request.method == "POST":
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
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

from __future__ import absolute_import
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from taskmanager.forms import TaskForm, UserRegistrationForm
from taskmanager.models import Task


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


def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            Task(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                assignee=form.cleaned_data["assignee"],
                due_date=form.cleaned_data["due_date"],
            ).save()
            return redirect('task_index')
    context = {
        'form': form
    }
    return render(request, 'create_task.html', context)


def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(initial={
        'title': task.title, 'description': task.description, 'assignee': task.assignee,
        'due_date': task.due_date
    })
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            Task(
                id=pk,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                assignee=form.cleaned_data["assignee"],
                due_date=form.cleaned_data["due_date"],
            ).save()
            return redirect('task_index')
        return render(request, 'edit_task.html', {'task': task})
    context = {
        'form': form
    }
    return render(request, 'edit_task.html', context)


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_index')
    return render(request, 'delete_task.html', {'task': task})


def redirect_task_index(request):
    return redirect('task_index')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            to_save = form.save(commit=False)
            to_save.username = username
            to_save.first_name = first_name
            to_save.last_name = last_name
            to_save.email = email
            to_save.password1 = password
            to_save.save()
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

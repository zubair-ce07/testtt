from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import TaskForm, UserRegistrationForm
from .models import Task


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
    users = [user.username for user in User.objects.all()]

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
        'task': task,
        'users': users
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
            form.save()
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('task_index')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Task
from .forms import TaskForm


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
            return HttpResponseRedirect('/tasks')
    context = {
        'form': form,
    }
    return render(request, 'create_task.html', context)


def edit_task(request, pk):
    task = Task.objects.get(id=pk)
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
            return HttpResponseRedirect("/tasks")
        return render(request, 'edit_task.html', {'task': task})
    return render(request, 'edit_task.html', {'task': task})


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect('/tasks')
    return render(request, 'delete_task.html', {'task': task})



def redirect_task_index(request):
    return HttpResponseRedirect("/tasks")

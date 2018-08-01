from django.urls import reverse, reverse_lazy
from django.views import generic

from taskmanager import models, forms


class Index(generic.ListView):
    model = models.Task
    template_name = "taskmanager/index.html"


class EditTask(generic.UpdateView):
    form_class = forms.TaskForm
    model = models.Task
    template_name = "taskmanager/edit.html"

    def get_success_url(self):
        return reverse('taskmanager:index')


class AddTask(generic.CreateView):
    form_class = forms.TaskForm
    model = models.Task
    template_name = "taskmanager/add.html"

    def get_success_url(self):
        return reverse('taskmanager:index')


class DeleteTask(generic.DeleteView):
    model = models.Task
    success_url = reverse_lazy('taskmanager:index')

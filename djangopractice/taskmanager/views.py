from django.contrib.auth import authenticate, login, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from taskmanager import models, forms


class SignUp(generic.CreateView):
    form_class = auth_forms.UserCreationForm
    success_url = reverse_lazy('taskmanager:index')
    template_name = 'taskmanager/signup.html'

    def form_valid(self, form):
        super(SignUp, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(self.success_url)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Index(generic.ListView):
    model = models.Task
    template_name = "taskmanager/index.html"


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditTask(generic.UpdateView):
    form_class = forms.TaskForm
    model = models.Task
    template_name = "taskmanager/edit.html"

    def get_success_url(self):
        return reverse('taskmanager:index')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddTask(generic.CreateView):
    form_class = forms.TaskForm
    model = models.Task
    template_name = "taskmanager/add.html"

    def get_form_kwargs(self):
        kwargs = super(AddTask, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('taskmanager:index')


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteTask(generic.DeleteView):
    model = models.Task
    success_url = reverse_lazy('taskmanager:index')

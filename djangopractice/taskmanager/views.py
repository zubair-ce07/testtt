from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from taskmanager import models, forms


@login_required(login_url='login')
def change_status(request, pk):
    task = models.Task.objects.get(id=pk)
    if task.status != 1:
        task.status = 1
    else:
        task.status = 0
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def validate_username(request):
    username = request.GET.get('username', None)
    username_exists = models.CustomUser.objects.filter(username__iexact=username).exists()
    data = {}
    if username_exists:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


class SignUp(generic.CreateView):
    form_class = forms.CustomUserCreationForm
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
class TaskDetails(generic.DetailView):
    model = models.Task
    template_name = "taskmanager/details.html"


@method_decorator(login_required(login_url='login'), name='dispatch')
class Index(generic.ListView):
    model = models.Task
    template_name = "taskmanager/index.html"

    def get_queryset(self):
        search_field = self.request.GET.get('search', None)
        if search_field:
            object_list = self.model.objects.filter(Q(title__icontains=search_field) |
                                                    Q(assignee__username__icontains=search_field))
        else:
            object_list = self.model.objects.all()
        return object_list


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditTask(generic.UpdateView):
    form_class = forms.TaskForm
    model = models.Task
    template_name = "taskmanager/edit.html"

    def get_success_url(self):
        return reverse('taskmanager:index')


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfile(generic.UpdateView):
    form_class = forms.CustomUserChangeForm
    model = models.CustomUser
    template_name = "taskmanager/profile.html"

    def get_success_url(self):
        return reverse('taskmanager:profile', args=(self.request.user.id, ))

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.kwargs['pk']:
            return super(EditProfile, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('taskmanager:profile_error'))


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddTask(generic.CreateView):
    form_class = forms.AddTaskForm
    exclude = ['status']
    template_name = "taskmanager/add.html"

    def get_form_kwargs(self):
        kwargs = super(AddTask, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('taskmanager:index')

    def get_form(self, form_class=forms.TaskForm):
        form = super(AddTask, self).get_form()
        form.fields.pop('status')
        return form


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteTask(generic.DeleteView):
    model = models.Task
    success_url = reverse_lazy('taskmanager:index')
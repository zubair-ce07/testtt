from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView, DeleteView, UpdateView, FormView

from .models import TodoList
from .forms import TodoAddForm


class AuthOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if not request.user.is_authenticated:
            return redirect(settings.LOGOUT_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class TodoListView(AuthOnlyView, FormView, ListView):
    template_name = "ListAndAdd.html"
    queryset = TodoList.objects.all()
    context_object_name = 'todos'
    form_class = TodoAddForm

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.content = todo.title + " -- " + todo.due_date.strftime("%-d-%-M-%Y")
        todo.save()
        return redirect('todoList')


class TodoListEdit(AuthOnlyView, UpdateView):
    success_url = "/todoList"
    form_class = TodoAddForm
    template_name = 'edit.html'
    queryset = TodoList.objects.all()


class TodoListDelete(AuthOnlyView, DeleteView):
    success_url = "/todoList"
    model = TodoList

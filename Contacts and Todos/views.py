from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login
from django.views import generic
from .forms import LoginForm, SignUpForm
from .models import User, Contact, Item, Todo


class Login(generic.View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'profile/home.html')
        context = {'form': form}
        return render(request, 'registration/login.html', context)


class SignUp(generic.View):

    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'profile/home.html')

        context = {'form': form}
        return render(request, 'registration/signup.html', context)


class Home(generic.TemplateView):
    template_name = 'profile/home.html'


class EditUser(generic.UpdateView):
    model = User
    template_name = 'profile/edit_user.html'
    fields = ['username', 'first_name', 'last_name', 'phone_number', 'profile_img', 'email', 'country']

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('manager:home')


class AddContact(generic.CreateView):
    template_name = 'profile/add_contact.html'
    model = Contact
    fields = ['name', 'email', 'phone_number', 'country', 'profile_img']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manager:contacts')


class EditContact(generic.UpdateView):
    model = Contact
    template_name = 'profile/edit_contact.html'
    fields = ['name', 'email', 'phone_number', 'country', 'profile_img']

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)

    def get_success_url(self):
        return reverse('manager:contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_id'] = self.kwargs.get('pk')
        return context


class Contacts(generic.TemplateView):
    template_name = 'profile/contacts.html'


class DeleteContact(generic.DeleteView):
    model = Contact
    template_name = 'profile/delete_contact.html'

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)

    def get_success_url(self):
        return reverse('manager:contacts')


class AddTodo(generic.CreateView):
    model = Todo
    template_name = 'profile/add_todo.html'
    fields = ['title', 'status']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manager:todos')


class EditTodo(generic.UpdateView):
    model = Todo
    template_name = 'profile/edit_todo.html'
    fields = ['title', 'status']

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def get_success_url(self):
        return reverse('manager:todos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_id'] = self.kwargs.get('pk')
        return context


class DeleteTodo(generic.DeleteView):
    model = Todo
    template_name = 'profile/delete_todo.html'

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def get_success_url(self):
        return reverse('manager:todos')


class Todos(generic.TemplateView):
    template_name = 'profile/todos.html'


class AddItem(generic.CreateView):
    model = Item
    template_name = 'profile/add_item.html'
    fields = ['text', 'status', 'due_date']

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.instance.todo = Todo.objects.get(id=pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_id'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse('manager:todos')


class EditItem(generic.UpdateView):
    lookup_field = 'pk'
    model = Item
    template_name = 'profile/edit_item.html'
    fields = ['text', 'status', 'due_date']

    def get_queryset(self):
        user = self.request.user
        todo_id = self.kwargs.get('todo_id')
        return Item.get_items(user, todo_id)

    def get_success_url(self):
        return reverse('manager:todos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_id'] = self.kwargs.get('todo_id')
        context['item_id'] = self.kwargs.get('pk')
        return context


class DeleteItem(generic.DeleteView):
    model = Item
    template_name = 'profile/delete_item.html'

    def get_queryset(self):
        user = self.request.user
        todo_id = self.kwargs.get('todo_id')
        return Item.get_items(user, todo_id)

    def get_success_url(self):
        return reverse('manager:todos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_id'] = self.kwargs.get('todo_id')
        context['item_id'] = self.kwargs.get('pk')
        return context



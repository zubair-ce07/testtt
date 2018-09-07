from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import UserForm
from .models import Profile


class IndexView(generic.DetailView):
    model = User
    template_name = 'profile/index.html'
    context_object_name = 'user'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(User, pk=self.request.user.pk)
        return reverse('users:login')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('users:index')

        return render(request, self.template_name, {'form': form})


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['address', 'age', 'profile_photo', 'gender']
    template_name = 'profile/generic_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') != self.request.user.pk:
            kwargs['pk'] = self.request.user.pk
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:index')


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile/generic_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.request.user.pk):
            form.add_error("email", "Email already exists")
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:index')

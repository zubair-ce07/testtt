from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import UpdateView
from validate_email import validate_email

from .forms import UserForm
from .models import Profile


class IndexDetailView(generic.DetailView):
    """
    Index detailed view to show user information
    """
    model = User
    template_name = 'profile/index.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(User, pk=self.request.user.pk)
        return reverse('users:login')

    def get_context_data(self, **kwargs):
        """
        Add `profile` to context data as well.
        """
        context = super(IndexDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class UserFormView(View):
    """
    User View to handle signup.
    """
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:index'))
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
    """
    Profile Update View
    """
    model = Profile
    fields = ['address', 'age', 'profile_photo', 'gender']
    template_name = 'profile/generic_form.html'

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return Profile.objects.get(user__pk=self.request.user.pk)
        return reverse('users:login')

    def get_success_url(self):
        return reverse_lazy('users:index')


class UserUpdate(UpdateView):
    """
    User update view
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:index')
    template_name = 'profile/generic_form.html'

    def form_valid(self, form):
        email = validate_email(form.cleaned_data['email'].strip())

        if not email:
            form.add_error("email", "Email is invalid")

        already_registered = User.objects.filter(email=email).exclude(pk=self.request.user.pk)

        if already_registered:
            form.add_error("email", "Email already exists")

        if form.errors:
            return self.render_to_response(self.get_context_data(form=form))

        password = form.cleaned_data['password'].strip()

        if password:
            self.request.user.set_password(password)
            update_session_auth_hash(self.request, self.request.user)

        form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user
        return reverse('users:login')

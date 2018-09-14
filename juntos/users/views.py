from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import UpdateView

from .forms import UserForm, ProfileForm


class IndexDetailView(generic.DetailView):
    """
    Index detailed view to show user information
    """
    template_name = 'users/profile/index.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UserFormView(View):
    """
    User View to handle signup.
    """
    form_class = UserForm
    template_name = 'users/registration/registration_form.html'

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
            if user and user.is_active:
                login(request, user)
                return redirect('users:index')

        return render(request, self.template_name, {'form': form})


class ProfileUpdate(UpdateView):
    """
    Profile Update View
    """
    fields = ['address', 'age', 'profile_photo', 'gender']
    template_name = 'users/profile/generic_form.html'
    success_url = reverse_lazy('users:index')

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserUpdate(UpdateView):
    """
    User update view
    """
    form_class = UserForm
    success_url = reverse_lazy('users:index')
    template_name = 'users/profile/generic_form.html'

    def form_valid(self, form):
        """This method is over ridden just because we need to call `update_session_auth_hash`
        otherwise `set_password` can be done in form's `save` method."""
        password = form.cleaned_data.pop('password')

        if password:
            self.request.user.set_password(password)
            update_session_auth_hash(self.request, self.request.user)

        form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user


@transaction.atomic
def update_profile(request):
    """
    To provide two forms to the user at a time, and let the user edit both at the same time.
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            password = user_form.cleaned_data['password'].strip()

            if password:
                request.user.set_password(password)
                update_session_auth_hash(request, request.user)

            user_form.save()
            profile_form.save()
            return redirect('users:index')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile/update_user_all_info.html', context={
        'user_form': user_form,
        'profile_form': profile_form
    })

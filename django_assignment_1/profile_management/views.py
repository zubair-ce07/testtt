from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class Home(TemplateView):
    template_name = 'profile_management/home.html'


class Index(LoginRequiredMixin, ListView):
    template_name = 'profile_management/index.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # TODO: Pagination
        return CustomUser.objects.filter(is_superuser=False)


class ProfileDetails(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile_management/detail.html'


class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = CustomUser
    fields = ['username', 'email', 'profile_photo']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'pk': self.object.pk})


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

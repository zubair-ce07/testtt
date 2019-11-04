from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        return CustomUser.objects.filter(is_superuser=False)


class ProfileDetails(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile_management/detail.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email', 'profile_photo']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'pk': self.object.pk})

    def test_func(self):
        is_self_user = self.request.user.pk == self.object.pk
        return self.request.user.is_superuser or is_self_user


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

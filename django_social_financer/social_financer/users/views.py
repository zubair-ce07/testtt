from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .forms import SignUpForm
# Create your views here.
#
class SignUpView(generic.FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    context_object_name = 'form'
    success_url = 'signup_successful/'

    def form_valid(self, form):
        return super().form_valid(form)

# class LoginView(generic.View):

def login_view(request):
    return HttpResponse("Login Page")
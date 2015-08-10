from django.shortcuts import render
from django.views.generic import View
from web.users.forms.login_form import LogInForm


class LogInView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name, dict(login_form=LogInForm()))

    def post(self, request):
        pass

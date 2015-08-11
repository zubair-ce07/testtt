from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.login_form import LogInForm


class LogInView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name, dict(login_form=LogInForm()))

    def post(self, request):
        response = None
        form = LogInForm(request.POST)
        response_message = ''

        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)

            if user:
                if user.is_active:

                    login(request, user)
                    response = redirect(reverse('account'))

                else:
                    response_message = 'Account has been disabled'
            else:
                response_message = 'Username or password is incorrect.'
        else:
            response_message = 'Please fill in the fields'

        if response_message:
            response = render(request, self.template_name, dict(msg=response_message, sign_in_form=form))

        return response

from django.shortcuts import render
from django.views.generic import View
from web.users.forms.sign_up_form import SignUpForm


class SignUpView(View):

    template_name = 'users/sign_up.html'

    def get(self, request):
        return render(request, self.template_name, dict(sign_up_form=SignUpForm()))

    def post(self, request):

        # sign_up_form = SignUpForm(request.POST)

        pass
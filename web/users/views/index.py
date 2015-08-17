from django.shortcuts import render
from django.views.generic import View
from web.users.forms.sign_up_form import SignUpForm


class IndexView(View):
    template_name = "users/index.html"

    def get(self, request):
        return render(request, self.template_name, dict(sign_up_form=SignUpForm()))
from braces.views import AnonymousRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import View

from web.account.forms import UserRegistrationForm


class HomepageView(AnonymousRequiredMixin, View):
    authenticated_redirect_url = "account:dashboard"
    template_name = 'web/homepage.html'

    def get(self, request):
        sign_up_form = UserRegistrationForm()
        login_form = AuthenticationForm()
        context = {
            "login_form": login_form,
            "sign_up_form": sign_up_form,
        }
        return render(request, 'web/homepage.html', context)

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import logout


class LogoutView(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


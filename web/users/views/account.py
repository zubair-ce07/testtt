from django.shortcuts import render
from django.views.generic import View


class AccountView(View):
    template_name = 'users/account.html'

    def get(self, request):
        return render(request, self.template_name, dict(name=request.user.get_full_name()))

    def post(self, request):
        pass
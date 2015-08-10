from django.views.generic import View


class AccountView(View):
    template_name = 'users/account.html'

    def get(self, request):
        pass

    def post(self, request):
        pass
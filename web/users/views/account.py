from django.shortcuts import render
from django.views.generic import View
from web.posts.forms.customized_search_form import CustomizedSearchForm


#TODO: This is your home/dashboard view. Not the account view. Please update it,
class AccountView(View):
    template_name = 'users/account.html'

    def get(self, request):
        return render(request, self.template_name, dict(customized_search_form=CustomizedSearchForm()))

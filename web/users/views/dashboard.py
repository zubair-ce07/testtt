from django.shortcuts import render
from django.views.generic import View
from web.posts.forms.customized_search_form import CustomizedSearchForm


class DashboardView(View):
    template_name = 'users/home.html'

    def get(self, request):
        return render(request, self.template_name, dict(customized_search_form=CustomizedSearchForm()))

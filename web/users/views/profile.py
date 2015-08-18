from django.shortcuts import render
from django.views.generic import View


#TODO: Merge edit profile page in this page.
class ProfileView(View):

    template_name = 'users/profile.html'

    def get(self, request):
        return render(request, self.template_name, dict(user=request.user))

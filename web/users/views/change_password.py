from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.change_password_form import ChangePasswordForm


class ChangePasswordView(View):

    template_name = 'users/change_password.html'

    def get(self, request):
        return render(request, self.template_name, dict(change_password_form=ChangePasswordForm(request.user)))

    def post(self, request):
        #TODO: No Need to declare this variable here.!
        response = None
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            response = redirect('/')
        else:
            response = render(request, self.template_name, dict(change_password_form=form))

        return response
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.change_password_form import ChangePasswordForm


class ChangePasswordView(View):

    template_name = 'users/change_password.html'

    def get(self, request):
        return render(request, self.template_name, dict(change_password_form=ChangePasswordForm(request.user)))

    def post(self, request):
        change_password_form = ChangePasswordForm(request.user, request.POST)
        if change_password_form.is_valid():
            user = request.user
            user.set_password(change_password_form.cleaned_data.get('new_password'))
            user.save()
            response = redirect(reverse('index'))
        else:
            response = render(request, self.template_name, dict(change_password_form=change_password_form))

        return response
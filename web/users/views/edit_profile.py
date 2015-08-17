from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.edit_profile_form import EditProfileForm
from web.users.models import User


class EditProfileView(View):

    template_name = 'users/edit_profile.html'

    def get(self, request):
        return render(request, self.template_name, dict(edit_profile_form=EditProfileForm()))

    def post(self, request):
        response = None
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.gender = form.cleaned_data.get('gender')
            user.dob = form.cleaned_data.get('date_of_birth')
            user.address.country = form.cleaned_data.get('country')
            user.address.city = str(form.cleaned_data.get('city'))
            user.address.street = form.cleaned_data.get('street_or_block')
            user.address.route = form.cleaned_data.get('route')
            user.address.zip_code = form.cleaned_data.get('zip_code')
            user.address.save()
            user.save()
            response = redirect(reverse('account'))
        else:
            response = render(request, self.template_name, dict(edit_profile_form=form))
        return response


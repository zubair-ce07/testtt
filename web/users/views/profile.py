from django.shortcuts import render
from django.views.generic import View

from web.users.forms.edit_profile_form import EditProfileForm


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, dict(edit_profile_form=EditProfileForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'gender': user.gender,
                     'date_of_birth': user.born_on, 'country': user.address.country, 'city': user.address.city,
                     'street_or_block': user.address.street, 'route': user.address.route,
                     'zip_code': user.address.zip_code})))

    def post(self, request):

        edit_profile_form = EditProfileForm(request.POST)
        if edit_profile_form.is_valid():
            user = request.user
            user.first_name = edit_profile_form.cleaned_data.get('first_name')
            user.last_name = edit_profile_form.cleaned_data.get('last_name')
            user.gender = edit_profile_form.cleaned_data.get('gender')
            user.born_on = edit_profile_form.cleaned_data.get('date_of_birth')
            user.address.country = edit_profile_form.cleaned_data.get('country')
            user.address.city = str(edit_profile_form.cleaned_data.get('city'))
            user.address.street = edit_profile_form.cleaned_data.get('street_or_block')
            user.address.route = edit_profile_form.cleaned_data.get('route')
            user.address.zip_code = edit_profile_form.cleaned_data.get('zip_code')
            user.address.save()
            user.save()
            response = render(request, self.template_name, dict(edit_profile_form=edit_profile_form))
        else:
            response = render(request, self.template_name, dict(edit_profile_form=edit_profile_form))
        return response
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.sign_up_form import SignUpForm
from web.users.models import Address, User


class SignUpView(View):
    template_name = 'users/index.html'

    def get(self, request):
        return render(request, self.template_name, dict(sign_up_form=SignUpForm()))

    def post(self, request):
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            email = sign_up_form.cleaned_data.get('email')
            password = sign_up_form.cleaned_data.get('password')
            first_name = sign_up_form.cleaned_data.get('first_name')
            last_name = sign_up_form.cleaned_data.get('last_name')
            country = sign_up_form.cleaned_data.get('country')
            city = sign_up_form.cleaned_data.get('city')
            street_or_block = sign_up_form.cleaned_data.get('street_or_block')
            route = sign_up_form.cleaned_data.get('route')
            zip_code = sign_up_form.cleaned_data.get('zip_code')
            state = sign_up_form.cleaned_data.get('state')
            gender = sign_up_form.cleaned_data.get('gender')
            date_of_birth = sign_up_form.cleaned_data.get('date_of_birth')

            address = Address(zip_code=zip_code, route=route, street=street_or_block, city=city, state=state,
                              country=country)
            address.save()
            User.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                     address=address, gender=gender, born_on=date_of_birth, password=password)
            response = redirect(reverse('login'))

        else:
            response = render(request, self.template_name, dict(sign_up_form=sign_up_form))

        return response

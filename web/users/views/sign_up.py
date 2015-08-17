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
        response = None
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            street_or_block = form.cleaned_data.get('street_or_block')
            route = form.cleaned_data.get('route')
            zip_code = form.cleaned_data.get('zip_code')
            state = form.cleaned_data.get('state')
            gender = form.cleaned_data.get('gender')
            date_of_birth = form.cleaned_data.get('date_of_birth')

            address = Address(zip_code=zip_code, route=route, street=street_or_block, city=city, state=state,
                              country=country)
            address.save()
            User.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                     address=address, gender=gender, dob=date_of_birth, password=password)
            response = redirect(reverse('login'))

        else:
            response = render(request, self.template_name, dict(sign_up_form=form))

        return response
